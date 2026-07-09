from typing import AsyncGenerator, List, Dict
from providers.ollama import OllamaProvider
from config.settings import settings

class ProviderEngine:
    """
    Abstraction layer managing LLM interactions.
    Defaults to Ollama. Capable of routing to optional cloud APIs if configured.
    """
    def __init__(self):
        # In the future, this can instantiate different providers based on settings
        self.provider = OllamaProvider()

    async def verify_system(self) -> bool:
        """Verifies that the provider and model are available."""
        is_connected = await self.provider.verify_connection()
        if not is_connected:
            return False
            
        model_exists = await self.provider.verify_model(settings.DEFAULT_MODEL)
        return model_exists

    async def stream_chat(self, messages: List[Dict[str, str]], model: str = None) -> AsyncGenerator[str, None]:
        """Routes a stream request to the active provider."""
        async for chunk in self.provider.stream_chat(messages, model):
            yield chunk

provider_engine = ProviderEngine()
