"""
Debug test to see what's causing the 500 errors
"""
import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_debug_generate_endpoint():
    """Debug test for text generation endpoint"""
    payload = {
        "prompt": "How is the NASDAQ market today?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/generate", json=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code != 200:
        print(f"Error details: {response.json() if response.text else 'No response body'}")
    else:
        data = response.json()
        assert "text" in data
        assert "model_id" in data


def test_debug_chat_endpoint():
    """Debug test for chat endpoint"""
    payload = {
        "messages": [
            {"role": "user", "content": "Hello, can you help me with investments?"}
        ]
    }
    response = client.post("/api/v1/chat", json=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code != 200:
        print(f"Error details: {response.json() if response.text else 'No response body'}")
    else:
        data = response.json()
        assert "message" in data
        assert data["message"]["role"] == "assistant"
