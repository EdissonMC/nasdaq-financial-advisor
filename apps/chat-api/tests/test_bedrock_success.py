"""
Tests for successful Bedrock operations
"""
import pytest
import json
from unittest.mock import patch, AsyncMock

from src.services.bedrock_service import BedrockService


@pytest.mark.asyncio
async def test_bedrock_generate_text_success(mock_bedrock_client, mock_bedrock_response, 
                                           sample_llm_request, mock_bedrock_stream_response):
    """Test successful text generation with Bedrock"""
    
    mock_response = mock_bedrock_stream_response(mock_bedrock_response)
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        response = await service.generate_text(sample_llm_request)
        
        # Verify response
        assert response.text == "Test response"
        assert response.usage["input_tokens"] == 10
        assert response.usage["output_tokens"] == 5
        assert response.model_id == "anthropic.claude-3-haiku-20240307-v1:0"
        
        # Verify API call
        mock_thread.assert_awaited_once()
        call_args = mock_thread.await_args
        
        assert call_args[0][0] == mock_bedrock_client.invoke_model
        assert 'modelId' in call_args[1]
        assert 'body' in call_args[1]
        
        body_data = json.loads(call_args[1]['body'])
        assert body_data['anthropic_version'] == "bedrock-2023-05-31"
        assert body_data['messages'][0]['content'] == "Test prompt"
        assert body_data['max_tokens'] == 100
        assert body_data['temperature'] == 0.7


@pytest.mark.asyncio
async def test_bedrock_chat_success(mock_bedrock_client, sample_chat_request, 
                                  mock_bedrock_stream_response):
    """Test successful chat with Bedrock"""
    
    response_data = {
        "content": [{"text": "Hello! How can I help?"}], 
        "usage": {"input_tokens": 5, "output_tokens": 8}
    }
    
    mock_response = mock_bedrock_stream_response(response_data)
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        response = await service.chat(sample_chat_request)
        
        # Verify response
        assert response.message.role == "assistant"
        assert response.message.content == "Hello! How can I help?"
        assert response.model_id == "anthropic.claude-3-haiku-20240307-v1:0"
        assert response.usage["input_tokens"] == 5
        assert response.usage["output_tokens"] == 8
        assert response.usage["conversation_turns"] == 1


@pytest.mark.asyncio
async def test_bedrock_multiple_messages_chat(mock_bedrock_client, mock_bedrock_stream_response):
    """Test chat with multiple messages in history"""
    from src.models.llm import ChatRequest, ChatMessage
    
    response_data = {
        "content": [{"text": "I'm doing well, thank you!"}], 
        "usage": {"input_tokens": 15, "output_tokens": 8}
    }
    
    mock_response = mock_bedrock_stream_response(response_data)
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        
        request = ChatRequest(
            messages=[
                ChatMessage(role="user", content="Hello"),
                ChatMessage(role="assistant", content="Hi there!"),
                ChatMessage(role="user", content="How are you?")
            ]
        )
        response = await service.chat(request)
        
        # Verify response
        assert response.message.content == "I'm doing well, thank you!"
        assert response.usage["conversation_turns"] == 3
        
        # Verify all messages were sent
        call_args = mock_thread.await_args
        body_data = json.loads(call_args[1]['body'])
        assert len(body_data['messages']) == 3
        assert body_data['messages'][2]['content'] == "How are you?"


@pytest.mark.parametrize("model_id,max_tokens", [
    ("anthropic.claude-3-haiku-20240307-v1:0", 100),
    ("anthropic.claude-3-sonnet-20240229-v1:0", 200),
])
@pytest.mark.asyncio
async def test_bedrock_different_models(mock_bedrock_client, mock_bedrock_response, 
                                      mock_bedrock_stream_response, model_id, max_tokens):
    """Test with different Claude models"""
    from src.models.llm import LLMRequest
    
    mock_response = mock_bedrock_stream_response(mock_bedrock_response)
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        request = LLMRequest(
            prompt="Test", 
            model_id=model_id,
            max_tokens=max_tokens
        )
        
        response = await service.generate_text(request)
        
        # Verify correct model was used
        assert response.model_id == model_id
        
        call_args = mock_thread.await_args
        assert call_args[1]['modelId'] == model_id
        
        body_data = json.loads(call_args[1]['body'])
        assert body_data['max_tokens'] == max_tokens
