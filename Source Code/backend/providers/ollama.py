import json
import httpx
from typing import AsyncGenerator, List, Dict
from config.settings import settings
from core.logger import get_logger

logger = get_logger("provider_ollama")

class OllamaProvider:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = settings.OLLAMA_TIMEOUT

    async def verify_connection(self) -> bool:
        """Check if Ollama daemon is reachable."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.base_url)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False

    async def verify_model(self, model_name: str) -> bool:
        """Check if the required model is pulled locally."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return any(m.get("name") == model_name for m in models)
                return False
        except Exception as e:
            logger.error(f"Failed to fetch models from Ollama: {e}")
            return False

    async def stream_chat(self, messages: List[Dict[str, str]], model: str = None) -> AsyncGenerator[str, None]:
        """Stream a chat completion from Ollama."""
        model_to_use = model or settings.DEFAULT_MODEL
        payload = {
            "model": model_to_use,
            "messages": messages,
            "stream": True
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    yield data["message"]["content"]
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to decode Ollama stream line: {line}")
        except httpx.TimeoutException:
            logger.error("Ollama generation timed out.")
            raise Exception("Provider timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama returned HTTP error: {e}")
            raise Exception(f"Provider error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected error communicating with Ollama: {e}")
            raise Exception("Provider connection error")
