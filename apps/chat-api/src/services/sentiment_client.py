import httpx
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SentimentClient:
    def __init__(self):
        self.base_url = os.getenv("SENTIMENT_API_URL", "http://localhost:8001")
        self.timeout = 10.0
    
    async def analyze_text(
        self, 
        text: str, 
        explain_with_llm: bool = False,
        user_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Analyze sentiment of a text"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/analyze",
                    json={
                        "text": text,
                        "explain_with_llm": explain_with_llm,
                        "user_id": user_id
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return None
    
    async def health_check(self) -> bool:
        """Check if service is available"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False

# Global instance
sentiment_client = SentimentClient()