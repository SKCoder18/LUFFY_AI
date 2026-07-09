import logging
import uuid
from typing import List, Dict, Any
from .sqlite_store import SQLiteStore
from .chroma_store import ChromaStore
from .embedding_provider import EmbeddingProvider
from .extractor import MemoryExtractor
from .queue import MemoryQueue
from ..rag.retriever import Retriever

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, sqlite_store: SQLiteStore, chroma_store: ChromaStore, embedding_provider: EmbeddingProvider, queue: MemoryQueue, retriever: Retriever, extractor: MemoryExtractor):
        self.sqlite = sqlite_store
        self.chroma = chroma_store
        self.embedder = embedding_provider
        self.queue = queue
        self.retriever = retriever
        self.extractor = extractor

    async def get_context(self, conversation_id: str, user_prompt: str) -> Dict[str, Any]:
        """
        Retrieves necessary context for the Prompt Builder.
        """
        try:
            pinned = await self.sqlite.get_pinned_memories()
            short_memory = await self.sqlite.get_recent_messages(conversation_id)
            summary = await self.sqlite.get_conversation_summary(conversation_id)
            
            # Retrieve long memory via Retriever
            retrieved = await self.retriever.retrieve(user_prompt, conversation_id)
            
            return {
                "pinned": pinned,
                "short_memory": short_memory,
                "summary": summary,
                "long_memory": retrieved.get("long_memory", []),
                "knowledge": retrieved.get("knowledge", [])
            }
        except Exception as e:
            logger.error(f"Error retrieving memory context: {str(e)}")
            return {"pinned": [], "short_memory": [], "summary": None, "long_memory": [], "knowledge": []}

    async def save_interaction(self, conversation_id: str, user_message: str, assistant_message: str):
        """
        Saves user and assistant messages, and initiates background extraction.
        """
        # Save messages to SQLite
        user_msg_id = str(uuid.uuid4())
        asst_msg_id = str(uuid.uuid4())
        await self.sqlite.save_message(user_msg_id, conversation_id, "user", user_message)
        await self.sqlite.save_message(asst_msg_id, conversation_id, "assistant", assistant_message)
        
        # Enqueue background processing for extraction and embedding
        await self.extract_and_store(conversation_id, user_message, assistant_message)

    async def extract_and_store(self, conversation_id: str, user_message: str, assistant_message: str):
        """
        Extracts meaningful memory and queues it for vectorization.
        """
        try:
            extracted = await self.extractor.extract(user_message)
            if extracted:
                mem_id = str(uuid.uuid4())
                extracted["id"] = mem_id
                
                # Check for semantic duplicate in SQLite (exact string match for now)
                duplicate = await self.sqlite.check_duplicate(extracted["content"])
                if duplicate:
                    logger.info(f"Duplicate memory detected. Merging {mem_id} into {duplicate['id']}.")
                    await self.sqlite.merge_memory(duplicate["id"], extracted)
                else:
                    await self.sqlite.save_memory_metadata(extracted)
                    # Enqueue for ChromaDB
                    await self.queue.enqueue(mem_id, extracted["content"], {"conversation_id": conversation_id, "category": extracted["category"], "importance": extracted["importance"], "source": extracted["source"]})
        except Exception as e:
            logger.error(f"Error extracting memory: {str(e)}")
