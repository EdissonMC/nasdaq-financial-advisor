"""
Factory para seleccionar el servicio LLM apropiado
"""
from ..core.config import settings
from .dummy_llm_service import dummy_llm_service
from .bedrock_service import bedrock_service


def get_llm_service():
    """
    Retorna el servicio LLM apropiado según la configuración
    
    Returns:
        Servicio LLM (dummy o bedrock)
    """
    if settings.llm_mode == "bedrock":
        return bedrock_service
    else:
        return dummy_llm_service


# Instancia del servicio actual
llm_service = get_llm_service()