import logging
import asyncio
from .sqlite_store import SQLiteStore
from .chroma_store import ChromaStore

logger = logging.getLogger(__name__)

class MemoryCleanup:
    def __init__(self, sqlite: SQLiteStore, chroma: ChromaStore):
        self.sqlite = sqlite
        self.chroma = chroma
        self._task = None

    async def start(self):
        self._task = asyncio.create_task(self._run_cleanup_cycle())
        logger.info("Memory cleanup background task started.")

    async def stop(self):
        if self._task:
            self._task.cancel()
            logger.info("Memory cleanup background task stopped.")

    async def _run_cleanup_cycle(self):
        while True:
            try:
                await asyncio.sleep(3600)  # Run hourly
                logger.info("Running memory cleanup cycle...")
                
                # Delete expired temporary memories (e.g., category='Temporary Context' older than 1 day)
                async with __import__('aiosqlite').connect(self.sqlite.db_path) as db:
                    await db.execute('''
                        DELETE FROM memories 
                        WHERE category = 'Temporary Context' AND created_at < datetime('now', '-1 day')
                    ''')
                    
                    # Delete messages from deleted conversations (orphaned)
                    await db.execute('''
                        DELETE FROM messages 
                        WHERE conversation_id NOT IN (SELECT id FROM conversations)
                    ''')
                    
                    await db.commit()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error during memory cleanup: {e}")
