"""
Modelos Pydantic para operaciones con LLM
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """Request para el LLM"""
    prompt: str = Field(..., description="Prompt para el LLM")
    max_tokens: Optional[int] = Field(1000, description="Máximo número de tokens")
    temperature: Optional[float] = Field(0.7, description="Temperatura para la generación")
    model_id: Optional[str] = Field(None, description="ID del modelo a usar")


class LLMResponse(BaseModel):
    """Response del LLM"""
    text: str = Field(..., description="Texto generado por el LLM")
    model_id: str = Field(..., description="Modelo usado")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Información de uso")
    
    
class ChatMessage(BaseModel):
    """Mensaje individual en una conversación"""
    role: str = Field(..., description="Rol del mensaje: user, assistant, system")
    content: str = Field(..., description="Contenido del mensaje")


class ChatRequest(BaseModel):
    """Request para chat conversacional"""
    messages: List[ChatMessage] = Field(..., description="Lista de mensajes")
    max_tokens: Optional[int] = Field(1000, description="Máximo número de tokens")
    temperature: Optional[float] = Field(0.7, description="Temperatura para la generación")
    model_id: Optional[str] = Field(None, description="ID del modelo a usar")


class ChatResponse(BaseModel):
    """Response del chat"""
    message: ChatMessage = Field(..., description="Mensaje de respuesta")
    model_id: str = Field(..., description="Modelo usado")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Información de uso")