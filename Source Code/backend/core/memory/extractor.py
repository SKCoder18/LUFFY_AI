import json
import logging
import httpx
from typing import Dict, Any, Optional
from ...config.settings import settings

logger = logging.getLogger(__name__)

class MemoryExtractor:
    """
    Extracts meaning from user prompts and classifies them using the Ollama model.
    """
    CATEGORIES = [
        "Preference", "Personal Fact", "Relationship", "Skill", 
        "Goal", "Task", "Knowledge", "Temporary Context"
    ]

    async def extract(self, text: str) -> Optional[Dict[str, Any]]:
        # Call Ollama to extract memory
        system_prompt = f"""You are a memory extraction assistant. Analyze the user's message and extract any meaningful facts, preferences, or knowledge that should be remembered long-term.
If the message is just temporary chat (e.g., "hello", "what is 2+2"), classify it as "Temporary Context".
Categories: {', '.join(self.CATEGORIES)}

Respond ONLY with a JSON object in this format:
{{
    "content": "extracted fact or summary",
    "category": "one of the categories",
    "importance": integer from 1 to 10
}}
If no meaningful memory is found, set category to "Temporary Context".
"""
        url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": settings.DEFAULT_MODEL,
            "prompt": text,
            "system": system_prompt,
            "stream": False,
            "format": "json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                result_text = data.get("response", "{}")
                
                try:
                    result = json.loads(result_text)
                    category = result.get("category", "Temporary Context")
                    if category == "Temporary Context" or result.get("importance", 1) < settings.MEMORY_IMPORTANCE_THRESHOLD:
                        return None # Do not store permanently
                        
                    return {
                        "content": result.get("content", text),
                        "category": category,
                        "importance": result.get("importance", 1),
                        "confidence": 0.9,
                        "source": "chat",
                        "memory_type": "extracted"
                    }
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse extractor JSON: {result_text}")
                    return None
        except Exception as e:
            logger.error(f"Failed to extract memory via Ollama: {str(e)}")
            return None
