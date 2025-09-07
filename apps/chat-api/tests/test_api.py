"""
Basic tests for the API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app

from src.services.bedrock_service import BedrockService
from src.models.llm import LLMRequest, ChatRequest, ChatMessage


client = TestClient(app)


def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["mode"] == "dummy"


def test_generate_endpoint():
    """Test text generation endpoint"""
    payload = {
        "prompt": "How is the NASDAQ market today?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model_id" in data


def test_chat_endpoint():
    """Test chat endpoint"""
    payload = {
        "messages": [
            {"role": "user", "content": "Hello, can you help me with investments?"}
        ]
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"]["role"] == "assistant"
    

@pytest.mark.asyncio
async def test_bedrock_generate_text():
    """Test generación de texto con Bedrock"""
    service = BedrockService()
    
    # Mock de la respuesta de Bedrock
    mock_body_data = b'{"content": [{"text": "Test response"}], "usage": {"input_tokens": 10, "output_tokens": 5}}'
    
    # Crear un mock más robusto para el body
    class MockStreamingBody:
        def read(self, *args, **kwargs):
            return mock_body_data
    
    mock_response = {
        'body': MockStreamingBody()
    }
    
    with patch.object(service, 'client') as mock_client:
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.return_value = mock_response
            
            request = LLMRequest(prompt="Test prompt")
            response = await service.generate_text(request)
            
            assert response.text == "Test response"
            assert response.usage["input_tokens"] == 10
            assert response.usage["output_tokens"] == 5


@pytest.mark.asyncio
async def test_bedrock_chat():
    """Test chat con Bedrock"""
    service = BedrockService()
    
    mock_body_data = b'{"content": [{"text": "Hello! How can I help?"}], "usage": {"input_tokens": 5, "output_tokens": 8}}'
    
    # Crear un mock más robusto para el body
    class MockStreamingBody:
        def read(self, *args, **kwargs):
            return mock_body_data
    
    mock_response = {
        'body': MockStreamingBody()
    }
    
    with patch.object(service, 'client') as mock_client:
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.return_value = mock_response
            
            request = ChatRequest(
                messages=[
                    ChatMessage(role="user", content="Hello")
                ]
            )
            response = await service.chat(request)
            
            assert response.message.role == "assistant"
            assert response.message.content == "Hello! How can I help?"