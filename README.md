# Smart Anki - AI-Powered Knowledge Base

An intelligent knowledge base application that uses spaced repetition and AI to help you learn effectively.

## Features
- Dark theme UI
- Category and subcategory management
- AI-powered content ingestion and fact-checking
- Spaced Repetition System (SRS)
- Multiple card types (Type-in, Reverse, Cloze)
- AI agent for interactive learning
- ADHD-friendly learning tools
- Category enable/disable functionality
- AI-powered Q&A system
- Authentication and user management
- AWS deployment with Terraform

## Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- AWS Account
- Terraform 1.0+
- Docker

## Local Development Setup
1. Clone the repository
2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Start the development servers:
   ```bash
   # Backend
   uvicorn app.main:app --reload
   
   # Frontend
   npm run dev
   ```

## Project Structure
```
smart-anki/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── docker/
└── README.md
```

## License
MIT
