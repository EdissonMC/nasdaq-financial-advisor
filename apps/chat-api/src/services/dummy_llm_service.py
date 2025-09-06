"""
Dummy LLM service for initial testing
"""
import random
import asyncio
from typing import List

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse, ChatMessage
from ..core.config import settings


class DummyLLMService:
    """LLM service with simulated responses"""
    
    def __init__(self):
        """Initialize the dummy service"""
        self.financial_responses = [
            "As a financial AI analyst, I can help you with market analysis, asset valuation and investment strategies.",
            "The NASDAQ market shows interesting trends. Are you interested in any specific sector?",
            "For fundamental analysis, we would need to review the company's financial statements.",
            "Risk metrics are essential for a balanced portfolio. What's your risk profile?",
            "Technical indicators suggest several patterns. Do you want to analyze any specific asset?"
        ]
    
    async def generate_text(self, request: LLMRequest) -> LLMResponse:
        """Simulate text generation"""
        # Simulate processing latency
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Select response
        response_text = random.choice(self.financial_responses)
        response_text += f"\n\n[Processing prompt: '{request.prompt[:50]}...']"
        
        return LLMResponse(
            text=response_text,
            model_id=request.model_id or settings.default_model_id,
            usage={
                "input_tokens": len(request.prompt.split()),
                "output_tokens": len(response_text.split()),
                "total_tokens": len(request.prompt.split()) + len(response_text.split())
            }
        )
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Simulate conversation"""
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Get last user message
        last_user_message = ""
        for message in reversed(request.messages):
            if message.role == "user":
                last_user_message = message.content
                break
        
        # Generate contextual response
        if "hello" in last_user_message.lower():
            response_text = "Hello! I'm your financial AI assistant. How can I help you today?"
        elif any(word in last_user_message.lower() for word in ['thanks', 'thank you']):
            response_text = "You're welcome! I'm here to help you with any financial queries."
        else:
            response_text = random.choice(self.financial_responses)
        
        assistant_message = ChatMessage(
            role="assistant",
            content=response_text
        )
        
        return ChatResponse(
            message=assistant_message,
            model_id=request.model_id or settings.default_model_id,
            usage={
                "input_tokens": sum(len(msg.content.split()) for msg in request.messages),
                "output_tokens": len(response_text.split()),
                "conversation_turns": len(request.messages)
            }
        )


# Global instance of the dummy service
dummy_llm_service = DummyLLMService()