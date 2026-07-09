import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
import logging
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class ChromaStore:
    def __init__(self):
        self.db_path = settings.CHROMA_DB_PATH
        self.client = chromadb.PersistentClient(path=self.db_path, settings=ChromaSettings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name="luffy_memories")
        logger.info("ChromaDB initialized successfully.")

    async def add_memory(self, memory_id: str, embedding: List[float], document: str, metadata: Dict[str, Any]):
        try:
            self.collection.add(
                ids=[memory_id],
                embeddings=[embedding],
                documents=[document],
                metadatas=[metadata]
            )
        except Exception as e:
            logger.error(f"Failed to add memory to ChromaDB: {str(e)}")
            raise e

    async def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )
            
            memories = []
            if results and results.get("ids") and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    memories.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i] if "documents" in results else "",
                        "metadata": results["metadatas"][0][i] if "metadatas" in results else {}
                    })
            return memories
        except Exception as e:
            logger.error(f"Failed to search ChromaDB: {str(e)}")
            return []
