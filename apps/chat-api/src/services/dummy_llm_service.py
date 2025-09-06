"""
Servicio LLM con respuestas dummy para testing inicial
"""
import random
import asyncio
from typing import List

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse, ChatMessage
from ..core.config import settings


class DummyLLMService:
    """Servicio LLM con respuestas simuladas"""
    
    def __init__(self):
        """Inicializa el servicio dummy"""
        self.financial_responses = [
            "Como analista financiero AI, te puedo ayudar con análisis de mercado, valoración de activos y estrategias de inversión.",
            "El mercado NASDAQ muestra tendencias interesantes. ¿Te interesa algún sector específico?",
            "Para análisis fundamental, necesitaríamos revisar los estados financieros de la empresa.",
            "Las métricas de riesgo son esenciales para una cartera balanceada. ¿Cuál es tu perfil de riesgo?",
            "Los indicadores técnicos sugieren varios patrones. ¿Quieres que analicemos algún activo específico?"
        ]
    
    async def generate_text(self, request: LLMRequest) -> LLMResponse:
        """Simula generación de texto"""
        # Simular latencia de procesamiento
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Seleccionar respuesta
        response_text = random.choice(self.financial_responses)
        response_text += f"\n\n[Procesando prompt: '{request.prompt[:50]}...']"
        
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
        """Simula conversación"""
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Obtener último mensaje del usuario
        last_user_message = ""
        for message in reversed(request.messages):
            if message.role == "user":
                last_user_message = message.content
                break
        
        # Generar respuesta contextual
        if "hola" in last_user_message.lower():
            response_text = "¡Hola! Soy tu asistente financiero AI. ¿En qué puedo ayudarte hoy?"
        elif any(word in last_user_message.lower() for word in ['gracias', 'thank']):
            response_text = "¡De nada! Estoy aquí para ayudarte con cualquier consulta financiera."
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


# Instancia global del servicio dummy
dummy_llm_service = DummyLLMService()