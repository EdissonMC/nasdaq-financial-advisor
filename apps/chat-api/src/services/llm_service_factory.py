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
    print(f"[DEBUG] get_llm_service() llamado. settings.llm_mode = {settings.llm_mode}")
    if settings.llm_mode == "bedrock":
        print("[DEBUG] Retornando bedrock_service")
        return bedrock_service
    else:
        print("[DEBUG] Retornando dummy_llm_service")
        return dummy_llm_service


# Instancia del servicio actual
llm_service = get_llm_service()