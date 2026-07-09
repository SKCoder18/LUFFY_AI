from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    sqlite_ok: bool
    chroma_ok: bool
    embedding_provider_ok: bool
    queue_ok: bool

@router.get("/health", response_model=HealthResponse)
async def health_check():
    # Placeholder for actual health checks against the memory subsystems
    return HealthResponse(
        status="ok",
        sqlite_ok=True,
        chroma_ok=True,
        embedding_provider_ok=True,
        queue_ok=True
    )
