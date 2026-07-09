import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.core.memory.sqlite_store import SQLiteStore

async def test():
    s = SQLiteStore()
    await s.init_db()
    print("Initial Settings:", await s.get_voice_settings())
    await s.save_voice_settings({'volume': 0.8, 'wake_word': 'hey luffy'})
    print("Updated Settings:", await s.get_voice_settings())

if __name__ == "__main__":
    asyncio.run(test())
