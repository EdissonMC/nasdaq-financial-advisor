"""
Script para verificar el funcionamiento del factory service
"""
import asyncio
import sys
sys.path.insert(0, 'src')

from src.services.llm_service_factory import get_llm_service
from src.models.llm import LLMRequest, ChatRequest, ChatMessage
from src.core.config import settings

async def test_factory_services():
    """Test del factory con ambos modos"""
    
    print(f"🔧 Modo actual: {settings.llm_mode}")
    print("=" * 50)
    
    # Test con modo actual
    service = get_llm_service()
    print(f"✅ Servicio obtenido: {type(service).__name__}")
    
    # Test generate
    print("\n📝 Testing generate_text...")
    try:
        request = LLMRequest(
            prompt="Hello, how are you?",
            max_tokens=50,
            temperature=0.7
        )
        response = await service.generate_text(request)
        print(f"✅ Generate response: {response.text[:100]}...")
        print(f"✅ Model ID: {response.model_id}")
    except Exception as e:
        print(f"❌ Error in generate: {e}")
    
    # Test chat
    print("\n💬 Testing chat...")
    try:
        chat_request = ChatRequest(
            messages=[
                ChatMessage(role="user", content="Hello!")
            ]
        )
        chat_response = await service.chat(chat_request)
        print(f"✅ Chat response: {chat_response.message.content[:100]}...")
        print(f"✅ Role: {chat_response.message.role}")
    except Exception as e:
        print(f"❌ Error in chat: {e}")

if __name__ == "__main__":
    asyncio.run(test_factory_services())
