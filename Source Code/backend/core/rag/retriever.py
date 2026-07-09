from typing import List, Dict, Any
import logging
from backend.core.memory.search_api import MemorySearchAPI
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self, search_api: MemorySearchAPI):
        self.search = search_api

    async def retrieve(self, query: str, conversation_id: str) -> Dict[str, List[Dict[str, Any]]]:
        # Priority: Relevant Long Memory > Knowledge Memory
        # Pinned and short are handled directly by memory manager/sqlite store
        long_memories = await self.search.semantic_search(query, limit=settings.RETRIEVAL_TOP_K)
        
        # Prioritize active conversation
        prioritized = sorted(long_memories, key=lambda x: x.get("metadata", {}).get("conversation_id") == conversation_id, reverse=True)
        
        # Filter for general knowledge memories
        knowledge = [m for m in long_memories if m.get("metadata", {}).get("category") == "Knowledge"]
        
        return {
            "long_memory": prioritized,
            "knowledge": knowledge
        }
