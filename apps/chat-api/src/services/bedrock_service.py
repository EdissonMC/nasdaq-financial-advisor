"""
Servicio AWS Bedrock para LLMs reales
"""
import json
import logging
import boto3
import asyncio
from typing import Dict, Any
from botocore.exceptions import ClientError

from ..models.llm import LLMRequest, LLMResponse, ChatRequest, ChatResponse, ChatMessage
from ..core.config import settings
from .prompt_template import get_financial_prompt


logger = logging.getLogger(__name__)


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
            logger.info("Bedrock client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Bedrock client: {e}")
            self.client = None
    
    def _process_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process Bedrock response to extract JSON data"""
        response_data = response['body'].read()
        if isinstance(response_data, bytes):
            response_data = response_data.decode('utf-8')
        return json.loads(response_data)
    
    def _extract_text_safely(self, response_body: Dict[str, Any]) -> str:
        """Extract text from response with error handling"""
        try:
            return response_body['content'][0]['text']
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Invalid response format from Bedrock: {e}")
            raise Exception(f"Invalid response format from Bedrock: {e}")
    
    
    
    
    
    
    async def generate_text(self, request: LLMRequest) -> LLMResponse:
        """Generar texto usando Bedrock"""
        if not self.client:
            raise Exception("Bedrock client not initialized")
             
        
        
        prompt = get_financial_prompt(
            user_query=request.prompt,
            context="Shares of apple are AAPL: $175, up 2% today, P/E ratio 25.4"
        )
        
        
                
        # Preparar payload para Claude
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens or settings.bedrock_max_tokens,
            "temperature": request.temperature or settings.bedrock_temperature,
            "messages": [
                {
                    "role": "user",
                    "content":prompt
                }
            ]
        }
        
        try:
            # Llamada a Bedrock
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId=request.model_id or settings.bedrock_model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps(body)
            )
            
            
       
             
             
            
            # Procesar respuesta
            response_body = self._process_response(response)
            text = self._extract_text_safely(response_body)
            
            return LLMResponse(
                text=text,
                model_id=request.model_id or settings.bedrock_model_id,
                usage={
                    "input_tokens": response_body['usage']['input_tokens'],
                    "output_tokens": response_body['usage']['output_tokens'],
                    "total_tokens": response_body['usage']['input_tokens'] + response_body['usage']['output_tokens']
                }
            )
            
            
            
            
            
            
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"Bedrock API error [{error_code}]: {error_message}")
            raise Exception(f"Bedrock API error [{error_code}]: {error_message}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Bedrock response: {e}")
            raise Exception(f"Invalid JSON response from Bedrock: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling Bedrock: {e}")
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
                contentType='application/json',
                accept='application/json',
                body=json.dumps(body)
            )
            
            response_body = self._process_response(response)
            text = self._extract_text_safely(response_body)
            
            assistant_message = ChatMessage(
                role="assistant",
                content=text
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
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"Bedrock API error [{error_code}]: {error_message}")
            raise Exception(f"Bedrock API error [{error_code}]: {error_message}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Bedrock response: {e}")
            raise Exception(f"Invalid JSON response from Bedrock: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling Bedrock: {e}")
            raise Exception(f"Error calling Bedrock: {e}")


# Instancia global del servicio Bedrock
bedrock_service = BedrockService()