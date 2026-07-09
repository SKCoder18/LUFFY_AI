import uuid
import logging
import httpx
from typing import Dict, Any, List
from backend.core.memory.sqlite_store import SQLiteStore
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, store: SQLiteStore):
        self.store = store

    async def create_conversation(self, title: str = "New Conversation") -> str:
        conv_id = str(uuid.uuid4())
        async with __import__('aiosqlite').connect(self.store.db_path) as db:
            await db.execute('''
                INSERT INTO conversations (id, title, summary)
                VALUES (?, ?, ?)
            ''', (conv_id, title, ""))
            await db.commit()
        logger.info(f"Created new conversation: {conv_id}")
        return conv_id

    async def rename_conversation(self, conv_id: str, new_title: str):
        async with __import__('aiosqlite').connect(self.store.db_path) as db:
            await db.execute('UPDATE conversations SET title = ? WHERE id = ?', (new_title, conv_id))
            await db.commit()

    async def delete_conversation(self, conv_id: str):
        async with __import__('aiosqlite').connect(self.store.db_path) as db:
            await db.execute('DELETE FROM messages WHERE conversation_id = ?', (conv_id,))
            await db.execute('DELETE FROM conversations WHERE id = ?', (conv_id,))
            await db.commit()

    async def list_conversations(self) -> List[Dict[str, Any]]:
        async with __import__('aiosqlite').connect(self.store.db_path) as db:
            db.row_factory = __import__('aiosqlite').Row
            cursor = await db.execute('SELECT id, title, summary, created_at, updated_at FROM conversations ORDER BY updated_at DESC')
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def generate_summary(self, conv_id: str) -> str:
        # Get recent messages to summarize
        messages = await self.store.get_recent_messages(conv_id, limit=20)
        if not messages:
            return ""
            
        chat_text = "\\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": settings.DEFAULT_MODEL,
            "prompt": chat_text,
            "system": "Summarize the following conversation in 1-2 concise sentences capturing the main topic.",
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                summary = data.get("response", "").strip()
                
                # Update DB
                async with __import__('aiosqlite').connect(self.store.db_path) as db:
                    await db.execute('UPDATE conversations SET summary = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (summary, conv_id))
                    await db.commit()
                    
                return summary
        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}")
            return ""
