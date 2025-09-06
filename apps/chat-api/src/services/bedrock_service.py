"""
Servicio AWS Bedrock para LLMs reales
"""
import json
import boto3
import asyncio
from typing import Dict, Any
from botocore.exceptions import ClientError

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse, ChatMessage
from ..core.config import settings


class BedrockService:
    """Servicio para interactuar con AWS Bedrock"""
    
    def __init__(self):
        """Inicializa el cliente de Bedrock"""
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente de AWS Bedrock"""
        try:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
            )
        except Exception as e:
            print(f"Error initializing Bedrock client: {e}")
            self.client = None
    
    async def generate_text(self, request: LLMRequest) -> LLMResponse:
        """Generar texto usando Bedrock"""
        if not self.client:
            raise Exception("Bedrock client not initialized")
        
        # Preparar payload para Claude
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens or settings.bedrock_max_tokens,
            "temperature": request.temperature or settings.bedrock_temperature,
            "messages": [
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
        }
        
        try:
            # Llamada a Bedrock
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId=request.model_id or settings.bedrock_model_id,
                body=json.dumps(body)
            )
            
            # Procesar respuesta
            response_body = json.loads(response['body'].read())
            
            return LLMResponse(
                text=response_body['content'][0]['text'],
                model_id=request.model_id or settings.bedrock_model_id,
                usage={
                    "input_tokens": response_body['usage']['input_tokens'],
                    "output_tokens": response_body['usage']['output_tokens'],
                    "total_tokens": response_body['usage']['input_tokens'] + response_body['usage']['output_tokens']
                }
            )
            
        except ClientError as e:
            raise Exception(f"Bedrock API error: {e}")
        except Exception as e:
            raise Exception(f"Error calling Bedrock: {e}")
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Chat conversacional usando Bedrock"""
        if not self.client:
            raise Exception("Bedrock client not initialized")
        
        # Convertir mensajes al formato de Claude
        messages = []
        for msg in request.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens or settings.bedrock_max_tokens,
            "temperature": request.temperature or settings.bedrock_temperature,
            "messages": messages
        }
        
        try:
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId=request.model_id or settings.bedrock_model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            assistant_message = ChatMessage(
                role="assistant",
                content=response_body['content'][0]['text']
            )
            
            return ChatResponse(
                message=assistant_message,
                model_id=request.model_id or settings.bedrock_model_id,
                usage={
                    "input_tokens": response_body['usage']['input_tokens'],
                    "output_tokens": response_body['usage']['output_tokens'],
                    "conversation_turns": len(request.messages)
                }
            )
            
        except ClientError as e:
            raise Exception(f"Bedrock API error: {e}")
        except Exception as e:
            raise Exception(f"Error calling Bedrock: {e}")


# Instancia global del servicio Bedrock
bedrock_service = BedrockService()