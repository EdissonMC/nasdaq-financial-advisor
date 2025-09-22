"""
Rutas actualizadas con factory service
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse
from ..services.llm_service_factory import get_llm_service
from ..core.config import settings
from ..db.session import get_db
from ..api.dependencies import get_optional_current_user, get_current_active_user
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
async def generate_text(request: LLMRequest, db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_optional_current_user)) -> LLMResponse:
    """Generar texto usando LLM"""
    try:
        print("...............GENERATE SIMPLE ANSWER............")
        print("request:", request)
        print(f"[DEBUG] settings.llm_mode = {settings.llm_mode}")
        service = get_llm_service()
        print(f"[DEBUG] LLM service type: {type(service)}")
        response = await service.generate_text(request)

        #response = await service.chat(request)

        print("response:", response)
        # Persistir historial si viene session_id
        if request.session_id:
            # Crear conversación si no existe
            conv = db.query(models.Conversation).filter(models.Conversation.session_id == request.session_id).first()
            if not conv:
                conv = models.Conversation(session_id=request.session_id, user_id=(current_user.id if current_user else None))
                db.add(conv)
                db.commit()
                db.refresh(conv)

            # Guardar mensaje del usuario
            db.add(models.Message(conversation_id=conv.id, role="user", content=request.prompt))
            # Guardar mensaje del asistente
            db.add(models.Message(conversation_id=conv.id, role="assistant", content=response.text))
            # actualizar timestamp de la conversación
            try:
                # set manual para disparar onupdate
                conv.title = conv.title
                db.add(conv)
            except Exception:
                pass
            db.commit()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")




# @router.post("/chat", response_model=ChatResponse)
# async def chat_conversation(request: ChatRequest, db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_optional_current_user)) -> ChatResponse:
#     """Mantener conversación con LLM"""
#     try:
#         service = get_llm_service()
#         response = await service.chat(request)
#         # Nota: En este endpoint no persistimos aún porque el frontend no lo usa
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
async def chat_conversation(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
) -> ChatResponse:
    try:
        print("...............GENERATE SIMPLE ANSWER............")
        print("request:", request)
        print(f"[DEBUG] settings.llm_mode = {settings.llm_mode}")
        service = get_llm_service()
        print(f"[DEBUG] LLM service type: {type(service)}")

        # Persistir historial si viene session_id
        if request.session_id:
            # Crear conversación si no existe
            conv = db.query(models.Conversation).filter(models.Conversation.session_id == request.session_id).first()
            if not conv:
                conv = models.Conversation(session_id=request.session_id, user_id=(current_user.id if current_user else None))
                db.add(conv)
                db.commit()
                db.refresh(conv)



            # Recuperar historial de mensajes
            msgs = (
                db.query(models.Message)
                .filter(models.Message.conversation_id == conv.id)
                .order_by(models.Message.created_at.asc())
                .all()
            )
            history = [{"role": m.role, "content": m.content} for m in msgs]

            # Llamar al servicio LLM con el historial
            response = await service.chat(history=history, request=request, currentMessage=request.message.content)
            
            # Guardar mensaje del usuario
            db.add(models.Message(conversation_id=conv.id, role="user", content=request.message.content))
            db.commit()
            
            # Guardar mensaje del asistente
            db.add(models.Message(conversation_id=conv.id, role="assistant", content=response.message.content))
            db.commit()
        else:
            # Si no hay session_id, solo responde normalmente
            response = await service.chat(request)

        print("response:", response)
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


@router.get("/chat/history")
async def get_chat_history(session_id: str, db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_optional_current_user)) -> Dict[str, Any]:
    """Obtiene el historial de mensajes por session_id"""
    conv = db.query(models.Conversation).filter(models.Conversation.session_id == session_id).first()
    if not conv:
        return {"messages": []}
    msgs = db.query(models.Message).filter(models.Message.conversation_id == conv.id).order_by(models.Message.created_at.asc()).all()
    return {
        "messages": [
            {"id": str(m.id), "role": m.role, "content": m.content, "timestamp": m.created_at.isoformat() if m.created_at else None}
            for m in msgs
        ]
    }

@router.delete("/chat/history")
async def delete_chat_history(session_id: str, db: Session = Depends(get_db), current_user: Optional[models.User] = Depends(get_optional_current_user)) -> Dict[str, Any]:
    """Elimina la conversación y sus mensajes por session_id"""
    conv = db.query(models.Conversation).filter(models.Conversation.session_id == session_id).first()
    if not conv:
        return {"deleted": 0}
    # Borrar mensajes primero
    db.query(models.Message).filter(models.Message.conversation_id == conv.id).delete()
    # Borrar conversación
    db.delete(conv)
    db.commit()
    return {"deleted": 1}


# ===== Conversaciones estilo ChatGPT =====
from pydantic import BaseModel
from typing import List

class ConversationCreate(BaseModel):
    session_id: str
    title: Optional[str] = None

class ConversationRename(BaseModel):
    title: str

@router.get("/conversations")
async def list_conversations(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Dict[str, Any]:
    rows = (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == current_user.id)
        .order_by(models.Conversation.updated_at.desc().nullslast(), models.Conversation.created_at.desc())
        .all()
    )
    return {
        "conversations": [
            {
                "session_id": r.session_id,
                "title": r.title or "Nueva conversación",
                "updated_at": (r.updated_at or r.created_at).isoformat() if (r.updated_at or r.created_at) else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    }

@router.post("/conversations")
async def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Dict[str, Any]:
    conv = db.query(models.Conversation).filter(models.Conversation.session_id == payload.session_id).first()
    if not conv:
        conv = models.Conversation(session_id=payload.session_id, user_id=current_user.id, title=payload.title)
        db.add(conv)
        db.commit()
        db.refresh(conv)
    return {"session_id": conv.session_id, "title": conv.title or "Nueva conversación"}

@router.patch("/conversations/{session_id}")
async def rename_conversation(session_id: str, payload: ConversationRename, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)) -> Dict[str, Any]:
    conv = (
        db.query(models.Conversation)
        .filter(models.Conversation.session_id == session_id, models.Conversation.user_id == current_user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv.title = payload.title
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"session_id": conv.session_id, "title": conv.title}


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