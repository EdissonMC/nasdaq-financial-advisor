"""
Shared fixtures for all tests
"""
import pytest
import io
import json
from unittest.mock import patch, Mock


@pytest.fixture
def mock_bedrock_response():
    """Fixture para respuesta mock de Bedrock"""
    return {
        "content": [{"text": "Test response"}], 
        "usage": {"input_tokens": 10, "output_tokens": 5}
    }


@pytest.fixture
def mock_bedrock_client():
    """Fixture para cliente mock de Bedrock"""
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_client_instance = Mock()
        mock_boto_client.return_value = mock_client_instance
        yield mock_client_instance


@pytest.fixture
def sample_llm_request():
    """Sample LLM request for testing"""
    from src.models.llm import LLMRequest
    return LLMRequest(prompt="Test prompt", max_tokens=100, temperature=0.7)


@pytest.fixture
def sample_chat_request():
    """Sample chat request for testing"""
    from src.models.llm import ChatRequest, ChatMessage
    return ChatRequest(
        messages=[
            ChatMessage(role="user", content="Hello")
        ],
        max_tokens=200,
        temperature=0.5
    )


@pytest.fixture
def mock_bedrock_stream_response():
    """Mock a realistic Bedrock response stream"""
    def _create_response(data):
        return {
            'body': io.BytesIO(json.dumps(data).encode('utf-8'))
        }
    return _create_response
