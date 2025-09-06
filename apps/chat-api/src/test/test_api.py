"""
Tests básicos para la API
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test del endpoint de health"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["mode"] == "dummy"


def test_generate_endpoint():
    """Test del endpoint de generación"""
    payload = {
        "prompt": "¿Cómo está el mercado NASDAQ hoy?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "model_id" in data


def test_chat_endpoint():
    """Test del endpoint de chat"""
    payload = {
        "messages": [
            {"role": "user", "content": "Hola, ¿puedes ayudarme con inversiones?"}
        ]
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"]["role"] == "assistant"