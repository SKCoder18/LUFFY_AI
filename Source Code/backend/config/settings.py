from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Provider Settings (Ollama)
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    DEFAULT_MODEL: str = "llama3.2:3b"
    OLLAMA_TIMEOUT: float = 60.0  # seconds
    
    # Memory Paths & Providers
    DATA_DIR: str = str(Path(__file__).parent.parent.parent / "data")
    SQLITE_DB_PATH: str = str(Path(__file__).parent.parent.parent / "data" / "luffy_memory.sqlite")
    CHROMA_DB_PATH: str = str(Path(__file__).parent.parent.parent / "data" / "chroma_db")
    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    
    # Memory Thresholds & Limits
    MEMORY_IMPORTANCE_THRESHOLD: int = 5
    EMBEDDING_RETRY_LIMIT: int = 3
    SHORT_MEMORY_HISTORY_LIMIT: int = 10  # Number of recent messages
    LONG_MEMORY_STORAGE_LIMIT: int = 1000 # Max items to store (concept)
    RETRIEVAL_TOP_K: int = 5
    MAX_PROMPT_AUGMENTATION_SIZE: int = 2000 # Max chars/tokens to augment
    
    # App Information
    APP_NAME: str = "LUFFY AI - Backend Core"
    VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
