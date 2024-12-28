from anthropic import Anthropic
from app.core.config import settings
import json

class AIService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
    async def process_content(self, content: str, category: str) -> dict:
        """
        Process and fact-check content, generate cards, and provide ADHD-friendly summaries
        """
        prompt = f"""
        Process this content for a knowledge base. The content is for category: {category}
        Content: {content}
        
        Please:
        1. Fact-check the content and provide corrections if needed
        2. Generate spaced repetition cards (mix of type-in, reverse, and cloze)
        3. Create an ADHD-friendly summary with key points
        4. Suggest related topics for further learning
        
        Format the response as JSON with these keys:
        - fact_check_results
        - cards
        - summary
        - related_topics
        """
        
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content)
    
    async def generate_questions(self, user_history: list, category: str) -> list:
        """
        Generate personalized questions based on user's learning history
        """
        prompt = f"""
        Generate personalized questions for a user studying {category}.
        User's recent performance:
        {json.dumps(user_history)}
        
        Create questions that:
        1. Focus on areas where the user needs more practice
        2. Include encouraging messages for ADHD support
        3. Mix different card types for engagement
        """
        
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content)
    
    async def answer_query(self, query: str, knowledge_base_content: str) -> str:
        """
        Answer user queries using the knowledge base content
        """
        prompt = f"""
        Answer this query using the provided knowledge base content.
        Query: {query}
        Knowledge Base Content: {knowledge_base_content}
        
        Please provide:
        1. A clear, concise answer
        2. References to specific parts of the knowledge base
        3. Suggestions for related topics to explore
        """
        
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content
