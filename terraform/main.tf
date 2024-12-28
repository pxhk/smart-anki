terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "smart-anki-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "smart-anki-cluster"
}

# ECR Repositories
resource "aws_ecr_repository" "backend" {
  name = "smart-anki-backend"
}

resource "aws_ecr_repository" "frontend" {
  name = "smart-anki-frontend"
}

# RDS Instance
resource "aws_db_instance" "postgres" {
  identifier           = "smart-anki-db"
  engine              = "postgres"
  engine_version      = "14"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_encrypted   = true
  
  db_name             = var.db_name
  username           = var.db_username
  password           = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  skip_final_snapshot    = true
}

# Redis for Session Management
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "smart-anki-redis"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis6.x"
  port                = 6379
  security_group_ids  = [aws_security_group.redis.id]
  subnet_group_name   = aws_elasticache_subnet_group.main.name
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "smart-anki-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets
}

# ECS Tasks and Services
resource "aws_ecs_task_definition" "backend" {
  family                   = "smart-anki-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512

  container_definitions = jsonencode([
    {
      name  = "backend"
      image = "${aws_ecr_repository.backend.repository_url}:latest"
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "POSTGRES_SERVER"
          value = aws_db_instance.postgres.endpoint
        },
        {
          name  = "REDIS_HOST"
          value = aws_elasticache_cluster.redis.cache_nodes[0].address
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "backend" {
  name            = "smart-anki-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 2

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = 8000
  }
}

# CloudWatch Logs
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/smart-anki"
  retention_in_days = 30
}

# Route 53 DNS (if domain is available)
resource "aws_route53_record" "app" {
  count   = var.domain_name != "" ? 1 : 0
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}
