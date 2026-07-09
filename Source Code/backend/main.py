import asyncio
from fastapi import FastAPI
from .api import health, chat
import logging
from .config.settings import settings

from .core.memory.sqlite_store import SQLiteStore
from .core.memory.chroma_store import ChromaStore
from .core.memory.embedding_provider import OllamaEmbeddingProvider
from .core.memory.extractor import MemoryExtractor
from .core.memory.queue import MemoryQueue
from .core.memory.cleanup import MemoryCleanup
from .core.memory.search_api import MemorySearchAPI
from .core.memory.conversation_manager import ConversationManager
from .core.memory.manager import MemoryManager
from .core.rag.retriever import Retriever

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
