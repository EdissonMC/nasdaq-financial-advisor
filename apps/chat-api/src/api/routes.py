from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ..db.session import get_db
from ..api.dependencies import get_optional_current_user
from ..db import models

# Router para las rutas del chat (existentes)
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

# Placeholder para endpoints de chat que agregaremos después
@router.post("/chat")
async def chat_endpoint(
    message: str,
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint de chat (temporal)
    """
    user_info = "anónimo"
    if current_user:
        user_info = f"usuario {current_user.email}"
    
    return {
        "response": f"Hola {user_info}, recibí tu mensaje: '{message}'",
        "user_authenticated": current_user is not None
    }