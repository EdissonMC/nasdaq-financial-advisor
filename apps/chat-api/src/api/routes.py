"""
API routes with dummy service
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse
from ..services.dummy_llm_service import dummy_llm_service

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "chat-api",
        "mode": "dummy"
    }


@router.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest) -> LLMResponse:
    """Generate text using LLM"""
    try:
        response = await dummy_llm_service.generate_text(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
async def chat_conversation(request: ChatRequest) -> ChatResponse:
    """Maintain conversation with LLM"""
    try:
        response = await dummy_llm_service.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@router.get("/models")
async def list_models() -> Dict[str, Any]:
    """List available models (dummy)"""
    return {
        "models": [
            {
                "id": "dummy-claude-3-haiku",
                "name": "Claude 3 Haiku (Dummy)",
                "provider": "dummy",
                "max_tokens": 4096
            }
        ],
        "mode": "dummy"
    }