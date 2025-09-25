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
from src.models.user import FeedbackRequest 
from src.services.sentiment_client import sentiment_client
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

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

        
        request_feedback = False

        if current_user:
            print(f"🔍 DEBUG: current_user existe = {current_user.id}")
            try:
                # Analizar sentimiento del mensaje del usuario
                user_sentiment = await sentiment_client.analyze_text(
                    text=request.message.content,
                    explain_with_llm=False,
                    user_id=current_user.id
                )
                print(f"🔍 DEBUG: user_sentiment completo = {user_sentiment}")
                
                has_sentiment = user_sentiment is not None
                compound_score = user_sentiment.get('sentiment_compound', 0) if user_sentiment else 0
                is_negative = compound_score < -0.1
                
                print(f"🔍 DEBUG: has_sentiment = {has_sentiment}")
                print(f"🔍 DEBUG: compound_score = {compound_score}")
                print(f"🔍 DEBUG: is_negative = {is_negative}")
                print(f"🔍 DEBUG: condición completa = {has_sentiment and is_negative}")
                
                if has_sentiment and is_negative:
                    request_feedback = True
                    print(f"😔 ACTIVANDO FEEDBACK para user {current_user.id}")
                else:
                    print(f"😊 NO activando feedback para user {current_user.id}")
                    
                print(f"🎯 RESULTADO FINAL: request_feedback = {request_feedback}")
                    
            except Exception as sentiment_error:
                logger.warning(f"⚠️ Sentiment analysis failed: {sentiment_error}")
                # Continuar sin sentiment analysis si falla
        
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
        
        
        response.request_feedback = request_feedback
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



@router.post("/feedback")
async def submit_user_feedback(
    feedback_data: FeedbackRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Receiving feedback from user {current_user.id}: {feedback_data.feedback_text[:50]}...")
        
        # Analizar sentiment del feedback usando el sentiment service
        feedback_sentiment = None
        triggered_analysis_id = None
        
        try:
            # Enviar feedback al sentiment service para análisis
            feedback_sentiment = await sentiment_client.analyze_text(
                text=feedback_data.feedback_text,
                explain_with_llm=True,
                user_id=current_user.id
            )
            
            # El sentiment service devuelve el ID del análisis guardado
            triggered_analysis_id = feedback_sentiment.get('id') if feedback_sentiment else None
            
            logger.info(f"📊 Feedback sentiment analyzed: {feedback_sentiment.get('sentiment_compound', 'N/A')}")
        except Exception as sentiment_error:
            logger.warning(f"⚠️ Sentiment analysis failed for feedback: {sentiment_error}")
        
        # Crear y guardar feedback en chat-api database
        new_feedback = models.Feedback(
            user_id=current_user.id,
            feedback_text=feedback_data.feedback_text,
            rating=feedback_data.rating or 3,
            triggered_by_analysis_id=triggered_analysis_id,  # ✅ ID del análisis en sentiment service
            feedback_sentiment_compound=feedback_sentiment.get('sentiment_compound') if feedback_sentiment else None,
            feedback_sentiment_analysis=feedback_sentiment.get('llm_explanation') if feedback_sentiment else None
        )
        
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        
        logger.info(f"✅ Feedback saved with ID: {new_feedback.id}")
        
        return {
            "status": "success",
            "message": "Thank you for your feedback! We'll use it to improve our service.",
            "feedback_id": new_feedback.id,
            "sentiment_analysis": feedback_sentiment  # Incluir análisis para debugging
        }
        
    except Exception as e:
        logger.error(f"❌ Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to process feedback")
    

# ✅ AÑADIR endpoint adicional en routes.py:

@router.get("/admin/feedback")
async def get_feedback_with_analysis(
    limit: int = 10,
    offset: int = 0,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get feedback list with sentiment analysis details"""
    try:
        query = db.query(models.Feedback)
        
        if resolved is not None:
            query = query.filter(models.Feedback.resolved == resolved)
            
        feedback_list = query.order_by(models.Feedback.created_at.desc())\
                           .offset(offset)\
                           .limit(limit)\
                           .all()
        
        # Para cada feedback, buscar el análisis en sentiment service
        enriched_feedback = []
        for feedback in feedback_list:
            feedback_data = {
                "id": feedback.id,
                "user_id": feedback.user_id,
                "feedback_text": feedback.feedback_text,
                "rating": feedback.rating,
                "category": feedback.category,
                "sentiment_compound": feedback.feedback_sentiment_compound,
                "sentiment_explanation": feedback.feedback_sentiment_analysis,
                "resolved": feedback.resolved,
                "created_at": feedback.created_at.isoformat() if feedback.created_at else None
            }
            
            # ✅ OPCIONAL: Obtener análisis completo del sentiment service
            if feedback.triggered_by_analysis_id:
                try:
                    # Llamar al sentiment service para obtener análisis completo
                    analysis_response = await sentiment_client.get_analysis_by_id(feedback.triggered_by_analysis_id)
                    feedback_data["original_analysis"] = analysis_response
                except Exception:
                    feedback_data["original_analysis"] = None
            
            enriched_feedback.append(feedback_data)
        
        return {
            "feedback": enriched_feedback,
            "total": db.query(models.Feedback).count()
        }
        
    except Exception as e:
        logger.error(f"Error fetching feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch feedback")

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