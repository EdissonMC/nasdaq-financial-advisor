"""
Basic configuration for initial development
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Dummy LLM Configuration
    default_model_id: str = "dummy-claude-3-haiku"
    default_max_tokens: int = 1000
    default_temperature: float = 0.7
    
    model_config = ConfigDict(env_file=".env")


# Global configuration instance
settings = Settings()