"""
Basic configuration for initial development
"""
from pydantic import ConfigDict, Field
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
    
    # Configuración de PostgreSQL (cargadas desde .env)
    postgres_user: str = Field(default="chatapi_user", env="POSTGRES_USER")
    postgres_password: str = Field(default="chatapi_password", env="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_db: str = Field(default="chatapi_db", env="POSTGRES_DB")
    
    # Configuración de la aplicación
    app_name: str = "Financial AI Chatbot API"
    environment: str = "development"
    
    # Configuración del modelo
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra='ignore'
    )
    
    def __init__(self, **kwargs):
        """Initialize settings and configure environment variables"""
        super().__init__(**kwargs)
        
        # Configure encoding environment variables after initialization
        os.environ['PGCLIENTENCODING'] = 'UTF8'
        os.environ['LC_ALL'] = 'C'
        os.environ['LANG'] = 'C'
    
    @property
    def database_url(self) -> str:
        """Construct database URL with proper encoding"""
        from urllib.parse import quote_plus
        
        # Validate required database fields
        if not self.postgres_user or not self.postgres_db:
            raise ValueError("Database user and database name are required")
        
        # URL encode the password to handle special characters
        encoded_password = quote_plus(self.postgres_password) if self.postgres_password else ""
        
        # Construct URL with encoding parameters
        base_url = f"postgresql://{self.postgres_user}:{encoded_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        
        # Add encoding parameters (remove options from URL, set in connect_args)
        encoding_params = "client_encoding=utf8"
        
        return f"{base_url}?{encoding_params}"


# Global configuration instance
settings = Settings()




if __name__ == "__main__":
    from pprint import pprint

    pprint(settings.model_dump())