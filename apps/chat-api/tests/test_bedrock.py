"""
Tests para el servicio Bedrock
"""
import pytest
import io
import json
from unittest.mock import patch, AsyncMock, Mock

from src.services.bedrock_service import BedrockService
from src.models.llm import LLMRequest, ChatRequest, ChatMessage


@pytest.mark.asyncio
async def test_bedrock_generate_text():
    """Test generación de texto con Bedrock"""
    
    # Mock response data
    response_data = {
        "content": [{"text": "Test response"}], 
        "usage": {"input_tokens": 10, "output_tokens": 5}
    }
    
    # Crear un mock realista usando BytesIO
    mock_body = io.BytesIO(json.dumps(response_data).encode('utf-8'))
    mock_response = {'body': mock_body}
    
    # Parchear boto3.client antes de crear el servicio
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_client_instance = Mock()
        mock_boto_client.return_value = mock_client_instance
        
        # Parchear asyncio.to_thread en el módulo específico
        with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.return_value = mock_response
            
            # Ahora crear el servicio (ya no intentará crear cliente real)
            service = BedrockService()
            
            request = LLMRequest(prompt="Test prompt", max_tokens=100, temperature=0.7)
            response = await service.generate_text(request)
            
            # Verificar la respuesta
            assert response.text == "Test response"
            assert response.usage["input_tokens"] == 10
            assert response.usage["output_tokens"] == 5
            assert response.model_id == "anthropic.claude-3-haiku-20240307-v1:0"
            
            # Verificar que asyncio.to_thread fue llamado correctamente
            mock_thread.assert_awaited_once()
            call_args = mock_thread.await_args
            
            # Verificar que se llamó con el cliente y los argumentos correctos
            assert call_args[0][0] == mock_client_instance.invoke_model
            assert 'modelId' in call_args[1]
            assert 'body' in call_args[1]
            
            # Verificar el body JSON
            body_data = json.loads(call_args[1]['body'])
            assert body_data['messages'][0]['content'] == "Test prompt"
            assert body_data['max_tokens'] == 100
            assert body_data['temperature'] == 0.7


@pytest.mark.asyncio
async def test_bedrock_chat():
    """Test chat con Bedrock"""
    
    # Mock response data
    response_data = {
        "content": [{"text": "Hello! How can I help?"}], 
        "usage": {"input_tokens": 5, "output_tokens": 8}
    }
    
    # Crear un mock realista usando BytesIO
    mock_body = io.BytesIO(json.dumps(response_data).encode('utf-8'))
    mock_response = {'body': mock_body}
    
    # Parchear boto3.client antes de crear el servicio
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_client_instance = Mock()
        mock_boto_client.return_value = mock_client_instance
        
        # Parchear asyncio.to_thread en el módulo específico
        with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.return_value = mock_response
            
            # Crear el servicio
            service = BedrockService()
            
            request = ChatRequest(
                messages=[
                    ChatMessage(role="user", content="Hello")
                ],
                max_tokens=200,
                temperature=0.5
            )
            response = await service.chat(request)
            
            # Verificar la respuesta
            assert response.message.role == "assistant"
            assert response.message.content == "Hello! How can I help?"
            assert response.model_id == "anthropic.claude-3-haiku-20240307-v1:0"
            assert response.usage["input_tokens"] == 5
            assert response.usage["output_tokens"] == 8
            assert response.usage["conversation_turns"] == 1
            
            # Verificar que asyncio.to_thread fue llamado correctamente
            mock_thread.assert_awaited_once()
            call_args = mock_thread.await_args
            
            # Verificar el body JSON para chat
            body_data = json.loads(call_args[1]['body'])
            assert len(body_data['messages']) == 1
            assert body_data['messages'][0]['role'] == "user"
            assert body_data['messages'][0]['content'] == "Hello"
            assert body_data['max_tokens'] == 200
            assert body_data['temperature'] == 0.5


@pytest.mark.asyncio
async def test_bedrock_service_initialization_error():
    """Test manejo de errores en inicialización del cliente"""
    
    # Simular error en boto3.client
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_boto_client.side_effect = Exception("AWS credentials not found")
        
        # El servicio debería manejar el error graciosamente
        service = BedrockService()
        assert service.client is None
        
        # Intentar usar el servicio debería fallar
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception, match="Bedrock client not initialized"):
            await service.generate_text(request)


@pytest.mark.asyncio 
async def test_bedrock_api_error():
    """Test manejo de errores de la API de Bedrock"""
    from botocore.exceptions import ClientError
    
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_client_instance = Mock()
        mock_boto_client.return_value = mock_client_instance
        
        # Simular error de Bedrock
        with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.side_effect = ClientError(
                error_response={'Error': {'Code': 'ValidationException', 'Message': 'Invalid model'}},
                operation_name='InvokeModel'
            )
            
            service = BedrockService()
            request = LLMRequest(prompt="Test")
            
            with pytest.raises(Exception, match="Bedrock API error"):
                await service.generate_text(request)