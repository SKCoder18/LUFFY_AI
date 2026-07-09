from typing import List, Dict, Any
from backend.core.memory.chroma_store import ChromaStore
from backend.core.memory.sqlite_store import SQLiteStore
from backend.core.memory.embedding_provider import EmbeddingProvider

class MemorySearchAPI:
    def __init__(self, chroma: ChromaStore, sqlite: SQLiteStore, embedder: EmbeddingProvider):
        self.chroma = chroma
        self.sqlite = sqlite
        self.embedder = embedder

    async def semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_emb = await self.embedder.get_embedding(query)
        if query_emb:
            return await self.chroma.search(query_emb, limit=limit)
        return []

    async def keyword_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with __import__('aiosqlite').connect(self.sqlite.db_path) as db:
            db.row_factory = __import__('aiosqlite').Row
            # Simple LIKE keyword search
            # Split query into words and search
            words = [f"%{w.strip()}%" for w in query.split() if len(w.strip()) > 3]
            if not words:
                return []
                
            sql = "SELECT id, category, content, importance, confidence FROM memories WHERE "
            conditions = ["content LIKE ?"] * len(words)
            sql += " OR ".join(conditions)
            sql += f" ORDER BY importance DESC LIMIT {limit}"
            
            cursor = await db.execute(sql, tuple(words))
            rows = await cursor.fetchall()
            
            return [{
                "id": r["id"],
                "content": r["content"],
                "metadata": {
                    "category": r["category"],
                    "importance": r["importance"],
                    "confidence": r["confidence"]
                }
            } for r in rows]

    async def hybrid_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Run both in parallel or sequential
        semantic_results = await self.semantic_search(query, limit=limit)
        keyword_results = await self.keyword_search(query, limit=limit)
        
        # Merge and deduplicate by ID
        seen = set()
        merged = []
        for r in semantic_results + keyword_results:
            if r["id"] not in seen:
                seen.add(r["id"])
                merged.append(r)
                
        # Basic sorting by importance (prefer metadata importance if available)
        merged.sort(key=lambda x: x.get("metadata", {}).get("importance", 1), reverse=True)
        return merged[:limit]
