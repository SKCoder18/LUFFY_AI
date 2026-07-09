import aiosqlite
import logging
import os
from typing import List, Dict, Any, Optional
from ...config.settings import settings

logger = logging.getLogger(__name__)

class SQLiteStore:
    def __init__(self):
        self.db_path = settings.SQLITE_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    category TEXT,
                    content TEXT,
                    importance INTEGER,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    version INTEGER DEFAULT 1,
                    source TEXT,
                    memory_type TEXT
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS pinned_memory (
                    id TEXT PRIMARY KEY,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
            logger.info("SQLite database initialized successfully.")

    async def get_recent_messages(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('''
                SELECT role, content FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (conversation_id, limit))
            rows = await cursor.fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]

    async def save_message(self, message_id: str, conversation_id: str, role: str, content: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO messages (id, conversation_id, role, content)
                VALUES (?, ?, ?, ?)
            ''', (message_id, conversation_id, role, content))
            await db.commit()

    async def get_conversation_summary(self, conversation_id: str) -> Optional[str]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT summary FROM conversations WHERE id = ?', (conversation_id,))
            row = await cursor.fetchone()
            return row[0] if row else None

    async def get_pinned_memories(self) -> List[str]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT content FROM pinned_memory ORDER BY created_at ASC')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]
            
    async def save_memory_metadata(self, memory: Dict[str, Any]):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR REPLACE INTO memories 
                (id, category, content, importance, confidence, version, source, memory_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory['id'], memory['category'], memory['content'], 
                memory.get('importance', 1), memory.get('confidence', 1.0),
                memory.get('version', 1), memory.get('source', 'system'),
                memory.get('memory_type', 'generic')
            ))
            await db.commit()

    async def check_duplicate(self, content: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute('SELECT id, version, access_count FROM memories WHERE content = ?', (content,))
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def merge_memory(self, memory_id: str, new_data: Dict[str, Any]):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                UPDATE memories 
                SET updated_at = CURRENT_TIMESTAMP, 
                    last_accessed = CURRENT_TIMESTAMP,
                    access_count = access_count + 1,
                    version = version + 1
                WHERE id = ?
            ''', (memory_id,))
            await db.commit()
