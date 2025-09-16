"""
Basic configuration for initial development
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    """Application configuration"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # Bedrock Configuration
    bedrock_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
    bedrock_max_tokens: int = 4096
    bedrock_temperature: float = 0.7
    
    # Default model ID (for dummy service compatibility)
    default_model_id: str = "dummy-claude-3-haiku"
    
    # Modo de operación (dummy o bedrock)
    llm_mode: str = "bedrock"  # dummy | bedrock
    
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

    llm_provider: str = "bedrock"
    
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
    environment: str = "development"
    
    # CORS (no se usa en el arranque; se deja por defecto en middleware)
# Global configuration instance
settings = Settings()