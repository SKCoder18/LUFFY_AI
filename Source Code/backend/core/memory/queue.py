import asyncio
import logging
from typing import Dict, Any
from backend.core.memory.embedding_provider import EmbeddingProvider
from backend.core.memory.chroma_store import ChromaStore
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class MemoryQueue:
    def __init__(self, provider: EmbeddingProvider, chroma: ChromaStore):
        self.provider = provider
        self.chroma = chroma
        self.queue = asyncio.Queue()
        self.max_retries = settings.EMBEDDING_RETRY_LIMIT
        self._task = None

    async def start(self):
        self._task = asyncio.create_task(self._process_queue())
        logger.info("Memory background queue started.")

    async def stop(self):
        if self._task:
            self._task.cancel()
            logger.info("Memory background queue stopped.")

    async def enqueue(self, memory_id: str, content: str, metadata: Dict[str, Any]):
        await self.queue.put({
            "id": memory_id,
            "content": content,
            "metadata": metadata,
            "retries": 0
        })

    async def _process_queue(self):
        while True:
            try:
                job = await self.queue.get()
                await self._process_job(job)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Queue processing error: {e}")

    async def _process_job(self, job: Dict[str, Any]):
        try:
            embedding = await self.provider.get_embedding(job["content"])
            if embedding:
                await self.chroma.add_memory(job["id"], embedding, job["content"], job["metadata"])
                logger.info(f"Successfully embedded and stored memory {job['id']}")
            else:
                raise ValueError("Empty embedding received.")
        except Exception as e:
            logger.warning(f"Failed to process job {job['id']}: {e}")
            if job["retries"] < self.max_retries:
                job["retries"] += 1
                await self.queue.put(job)
            else:
                logger.error(f"Permanently failed to embed memory {job['id']} after {self.max_retries} retries.")
