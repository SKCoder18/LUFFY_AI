from typing import List, Protocol
import httpx
from backend.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingProvider(Protocol):
    async def get_embedding(self, text: str) -> List[float]:
        ...

class OllamaEmbeddingProvider:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.EMBEDDING_MODEL

    async def get_embedding(self, text: str) -> List[float]:
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT)
                response.raise_for_status()
                data = response.json()
                return data.get("embedding", [])
        except Exception as e:
            logger.error(f"Failed to generate embedding with Ollama: {str(e)}")
            raise e
