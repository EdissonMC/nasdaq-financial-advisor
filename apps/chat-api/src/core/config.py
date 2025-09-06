"""
Configuración básica para desarrollo inicial
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Dummy LLM Configuration
    default_model_id: str = "dummy-claude-3-haiku"
    default_max_tokens: int = 1000
    default_temperature: float = 0.7
    
    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()