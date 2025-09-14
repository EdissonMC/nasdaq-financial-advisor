"""
Rutas actualizadas con factory service
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse
from ..services.llm_service_factory import get_llm_service
from ..core.config import settings
from ..db.session import get_db
from ..api.dependencies import get_optional_current_user
from ..db import models

router = APIRouter()

@router.get("/")
async def root():
    """Endpoint raíz del API"""
    return {
        "message": "Financial AI Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }

@router.get("/chat/health")
async def chat_health():
    """Health check del servicio de chat"""
    return {
        "status": "healthy",
        "service": "chat",
        "message": "Servicio de chat funcionando correctamente"
    }

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "chat-api",
        "mode": settings.llm_mode
    }


@router.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest) -> LLMResponse:
    """Generar texto usando LLM"""
    try:
        service = get_llm_service()
        response = await service.generate_text(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
async def chat_conversation(request: ChatRequest) -> ChatResponse:
    """Mantener conversación con LLM"""
    try:
        service = get_llm_service()
        response = await service.chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@router.get("/models")
async def list_models() -> Dict[str, Any]:
    """Lista modelos disponibles"""
    if settings.llm_mode == "bedrock":
        return {
            "models": [
                {
                    "id": "anthropic.claude-3-haiku-20240307-v1:0",
                    "name": "Claude 3 Haiku",
                    "provider": "aws-bedrock",
                    "max_tokens": 4096
                },
                {
                    "id": "anthropic.claude-3-sonnet-20240229-v1:0",
                    "name": "Claude 3 Sonnet",
                    "provider": "aws-bedrock",
                    "max_tokens": 4096
                }
            ],
            "mode": "bedrock"
        }
    else:
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


@router.post("/switch-mode")
async def switch_mode(mode: str) -> Dict[str, str]:
    """Cambiar entre modo dummy y bedrock"""
    if mode not in ["dummy", "bedrock"]:
        raise HTTPException(status_code=400, detail="Mode must be 'dummy' or 'bedrock'")
    
    # Nota: En producción esto debería actualizar la configuración persistente
    settings.llm_mode = mode
    
    return {
        "message": f"LLM mode switched to {mode}",
        "current_mode": settings.llm_mode
    }