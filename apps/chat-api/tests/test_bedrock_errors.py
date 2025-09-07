"""
Tests for Bedrock error handling and edge cases
"""
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from botocore.exceptions import ClientError

from src.services.bedrock_service import BedrockService
from src.models.llm import LLMRequest


@pytest.mark.asyncio
async def test_bedrock_empty_response(mock_bedrock_client, mock_bedrock_stream_response):
    """Test handling of empty response"""
    
    response_data = {
        "content": [], 
        "usage": {"input_tokens": 5, "output_tokens": 0}
    }
    
    mock_response = mock_bedrock_stream_response(response_data)
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        request = LLMRequest(prompt="Test")
        
        # Should fail when trying to access content[0]
        with pytest.raises(Exception):
            await service.generate_text(request)


@pytest.mark.asyncio
async def test_bedrock_malformed_response(mock_bedrock_client):
    """Test handling of malformed response"""
    import io
    
    mock_body = io.BytesIO(b'invalid json')
    mock_response = {'body': mock_body}
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.return_value = mock_response
        
        service = BedrockService()
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception, match="Invalid JSON response from Bedrock"):
            await service.generate_text(request)


@pytest.mark.asyncio
async def test_bedrock_service_initialization_error():
    """Test handling of client initialization errors"""
    
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_boto_client.side_effect = Exception("AWS credentials not found")
        
        # Service should handle error gracefully
        service = BedrockService()
        
        # Verify client is None but service doesn't fail during creation
        assert service.client is None
        
        # Verify specific and clear error message
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception) as exc_info:
            await service.generate_text(request)
        
        assert "Bedrock client not initialized" in str(exc_info.value)


@pytest.mark.asyncio 
async def test_bedrock_api_error(mock_bedrock_client):
    """Test handling of Bedrock API errors"""
    
    # Simulate Bedrock error
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        error_response = {
            'Error': {
                'Code': 'ValidationException', 
                'Message': 'Invalid model'
            }
        }
        mock_thread.side_effect = ClientError(error_response, 'InvokeModel')
        
        service = BedrockService()
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception) as exc_info:
            await service.generate_text(request)
        
        # Verify error contains useful information
        assert "Bedrock API error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_bedrock_timeout(mock_bedrock_client):
    """Test timeout handling"""
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.side_effect = asyncio.TimeoutError("Request timeout")
        
        service = BedrockService()
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception, match="Error calling Bedrock"):
            await service.generate_text(request)


@pytest.mark.asyncio
async def test_bedrock_invalid_model_parameters():
    """Test handling of invalid model parameters"""
    
    with patch('src.services.bedrock_service.boto3.client') as mock_boto_client:
        mock_client_instance = mock_boto_client.return_value
        
        with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            error_response = {
                'Error': {
                    'Code': 'ValidationException',
                    'Message': 'Invalid max_tokens value'
                }
            }
            mock_thread.side_effect = ClientError(error_response, 'InvokeModel')
            
            service = BedrockService()
            
            # Test with invalid max_tokens
            request = LLMRequest(prompt="Test", max_tokens=-1)
            
            with pytest.raises(Exception) as exc_info:
                await service.generate_text(request)
            
            assert "Bedrock API error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_bedrock_network_error(mock_bedrock_client):
    """Test network connectivity issues"""
    from botocore.exceptions import EndpointConnectionError
    
    with patch('src.services.bedrock_service.asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
        mock_thread.side_effect = EndpointConnectionError(
            endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com"
        )
        
        service = BedrockService()
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(Exception, match="Error calling Bedrock"):
            await service.generate_text(request)
