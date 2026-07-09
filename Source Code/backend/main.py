import asyncio
from fastapi import FastAPI
from backend.api import health, chat
import logging
from backend.config.settings import settings

from backend.core.memory.sqlite_store import SQLiteStore
from backend.core.memory.chroma_store import ChromaStore
from backend.core.memory.embedding_provider import OllamaEmbeddingProvider
from backend.core.memory.extractor import MemoryExtractor
from backend.core.memory.queue import MemoryQueue
from backend.core.memory.cleanup import MemoryCleanup
from backend.core.memory.search_api import MemorySearchAPI
from backend.core.memory.conversation_manager import ConversationManager
from backend.core.memory.manager import MemoryManager
from backend.core.rag.retriever import Retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LUFFY AI - Backend Core", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing LUFFY Memory Subsystems...")
    
    # Initialize Core Stores
    sqlite_store = SQLiteStore()
    await sqlite_store.init_db()
    
    chroma_store = ChromaStore()
    
    # Initialize Providers & APIs
    embedder = OllamaEmbeddingProvider()
    search_api = MemorySearchAPI(chroma_store, sqlite_store, embedder)
    extractor = MemoryExtractor()
    
    # Initialize Queue & Background Tasks
    queue = MemoryQueue(embedder, chroma_store)
    await queue.start()
    
    cleanup = MemoryCleanup(sqlite_store, chroma_store)
    await cleanup.start()
    
    # Initialize Managers
    retriever = Retriever(search_api)
    conv_manager = ConversationManager(sqlite_store)
    
    memory_manager = MemoryManager(
        sqlite_store=sqlite_store,
        chroma_store=chroma_store,
        embedding_provider=embedder,
        queue=queue,
        retriever=retriever,
        extractor=extractor
    )
    
    # Attach to App State
    app.state.sqlite_store = sqlite_store
    app.state.chroma_store = chroma_store
    app.state.queue = queue
    app.state.cleanup = cleanup
    app.state.memory_manager = memory_manager
    app.state.conv_manager = conv_manager
    app.state.embedder = embedder

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down LUFFY Memory Subsystems...")
    await app.state.queue.stop()
    await app.state.cleanup.stop()

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
