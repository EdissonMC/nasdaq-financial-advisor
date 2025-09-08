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

    llm_mode: str = "bedrock"  # bedrock

    
    
    model_config = ConfigDict(env_file=".env")


# Global configuration instance
settings = Settings()