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
from .pinecone_service import PineconeService

logger = logging.getLogger(__name__)


class BedrockService:
    """Servicio para interactuar con AWS Bedrock"""
    
    def __init__(self):
        """Inicializa el cliente de Bedrock"""
        self.client = None
        self._initialize_client()
        self.pinecone_service = PineconeService()
    
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
        
        print("=== CAMBIO DE PRUEBA EN BEDROCK_SERVICE ===")    
        print("...............GENERATE SIMPLE ANSWER WITH BEDROCK AWS............")
        
        prompt = get_financial_prompt(
            user_query=request.prompt,
            context=""  # Sin contexto hardcodeado
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
    
    
    
    
    
    
    
    
 

    # async def chat(self, request: ChatRequest) -> ChatResponse:
    #     """Chat conversacional usando Bedrock"""
    #     if not self.client:
    #         raise Exception("Bedrock client not initialized")
        
    #     # Convertir mensajes al formato de Claude
    #     # Obtiene el historial de mensajes por session_id
    #     conv = db.query(models.Conversation).filter(models.Conversation.session_id == session_id).first()
    #     if not conv:
    #         return {"messages": []}
    #     msgs = db.query(models.Message).filter(models.Message.conversation_id == conv.id).order_by(models.Message.created_at.asc()).all()
    #     print("HISTORIAL DE MENSAJES ENCONTRADOS:"
    #           for m in msgs:)
        
        
    #     messages = []
    #     for msg in request.messages:
    #         messages.append({
    #             "role": msg.role,
    #             "content": msg.content
    #         })
        
    #     body = {
    #         "anthropic_version": "bedrock-2023-05-31",
    #         "max_tokens": request.max_tokens or settings.bedrock_max_tokens,
    #         "temperature": request.temperature or settings.bedrock_temperature,
    #         "messages": messages
    #     }
        
    #     try:
    #         response = await asyncio.to_thread(
    #             self.client.invoke_model,
    #             modelId=request.model_id or settings.bedrock_model_id,
    #             contentType='application/json',
    #             accept='application/json',
    #             body=json.dumps(body)
    #         )
            
    #         response_body = self._process_response(response)
    #         text = self._extract_text_safely(response_body)
            
    #         assistant_message = ChatMessage(
    #             role="assistant",
    #             content=text
    #         )
            
    #         return ChatResponse(
    #             message=assistant_message,
    #             model_id=request.model_id or settings.bedrock_model_id,
    #             usage={
    #                 "input_tokens": response_body['usage']['input_tokens'],
    #                 "output_tokens": response_body['usage']['output_tokens'],
    #                 "conversation_turns": len(request.messages)
    #             }
    #         )
            
    #     except ClientError as e:
    #         error_code = e.response.get('Error', {}).get('Code', 'Unknown')
    #         error_message = e.response.get('Error', {}).get('Message', str(e))
    #         logger.error(f"Bedrock API error [{error_code}]: {error_message}")
    #         raise Exception(f"Bedrock API error [{error_code}]: {error_message}")
    #     except json.JSONDecodeError as e:
    #         logger.error(f"Failed to parse Bedrock response: {e}")
    #         raise Exception(f"Invalid JSON response from Bedrock: {e}")
    #     except Exception as e:
    #         logger.error(f"Unexpected error calling Bedrock: {e}")
    #         raise Exception(f"Error calling Bedrock: {e}")


    async def chat(self, request: ChatRequest, history: list = None, currentMessage: str = "") -> ChatResponse:
        """Chat conversacional usando Bedrock con historial"""
        if not self.client:
            raise Exception("Bedrock client not initialized")
        
        # Usar el historial pasado desde el endpoint, o los mensajes del request como fallback
        
        # Recuperar contexto relevante de Pinecone para enriquecer la respuesta
        try:
            context = self.pinecone_service.search(currentMessage, top_k=2)
            logger.info("Contexto recuperado de Pinecone para enriquecer respuesta")
            logger.debug(f"Contexto: {context}")
        except Exception as e:
            logger.error(f"Error getting context from Pinecone: {e}", exc_info=True)
            context = "No context available due to Pinecone error"
        
        current_message_formated=get_financial_prompt(user_query =currentMessage, context=context) 
        message_format = [
            {
                "role": "user", 
             
                "content": current_message_formated
             }
        ]
        
        
        # print("***"*30)
        # print("MENSAJE FORMATEADO PARA EL PROMPT:") 
        # print(current_message_formated)
        # print("***"*30)
        
        messages = []

        if history:
            # Usar el historial proporcionado
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Siempre agregar el mensaje actual formateado
        messages.extend(message_format)
        print("Mensajes finales enviados a Bedrock:")
        print(messages)

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": request.max_tokens or settings.bedrock_max_tokens,
            "temperature": request.temperature or settings.bedrock_temperature,
            "messages": messages
        }
        
        try:
            logger.info(f"Sending request to Bedrock with model: {request.model_id or settings.bedrock_model_id}")
            logger.info(f"Request body: {json.dumps(body, indent=2)}")
            
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId=request.model_id or settings.bedrock_model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps(body)
            )
            
            logger.info(f"Raw response from Bedrock: {response}")
            response_body = self._process_response(response)
            logger.info(f"Parsed response body: {json.dumps(response_body, indent=2)}")
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
                    "conversation_turns": len(messages)
                }
            )
            
            
            # SIMULACIÓN DE RESPUESTA
            # text="****This is a placeholder response from Bedrock.*******"
            # assistant_message = ChatMessage(
            #     role="assistant",
            #     content=text
            # )
            
            # return ChatResponse(
            #     message=assistant_message,
            #     model_id=request.model_id or settings.bedrock_model_id,
            #     usage={
            #         "input_tokens": 100,
            #         "output_tokens": 600,
            #         "conversation_turns": len(messages)
            #     }
            # )
            
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"Bedrock ClientError [{error_code}]: {error_message}")
            logger.error(f"Full error response: {e.response}")
            # Re-raise the original exception for full stack trace
            raise e
        except Exception as e:
            logger.error(f"Unexpected error calling Bedrock: {e}")
            logger.error(f"Full exception details:", exc_info=True)
            # Re-raise the original exception for full stack trace
            raise e



























# Instancia global del servicio Bedrock
bedrock_service = BedrockService()