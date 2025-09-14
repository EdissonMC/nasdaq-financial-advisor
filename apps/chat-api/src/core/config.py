from pydantic_settings import BaseSettings  # ✅ CAMBIADO: era pydantic.BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Configuración existente del LLM
    default_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    llm_provider: str = "dummy"
    
    # Configuración de autenticación
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    
    # Configuración de PostgreSQL
    postgres_user: str = "chatapi_user"
    postgres_password: str = "chatapi_password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "chatapi_db"
    
    # URL de base de datos construida automáticamente
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Configuración de la aplicación
    app_name: str = "Financial AI Chatbot API"
    debug: bool = True
    environment: str = "development"
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()