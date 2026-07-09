from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.chat import ChatRequest, ErrorResponse
from core.reasoning_engine import reasoning_engine
from core.provider_engine import provider_engine
from core.logger import get_logger

logger = get_logger("api_routes")
router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check():
    """Health endpoint to verify API status and provider connectivity."""
    is_ready = await provider_engine.verify_system()
    if is_ready:
        return {"status": "healthy", "provider": "connected"}
    else:
        logger.error("Health check failed: Provider not ready.")
        raise HTTPException(
            status_code=503, 
            detail={"error": "Service Unavailable", "details": "Ollama or configured model is unreachable"}
        )

@router.post("/chat", response_class=StreamingResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint to stream AI responses."""
    logger.info("Received chat request")
    
    async def event_generator():
        messages = [msg.model_dump() for msg in request.messages]
        try:
            async for chunk in reasoning_engine.process_request(messages, request.model):
                yield chunk
        except Exception as e:
            logger.error(f"Error during stream generation: {str(e)}")
            # For streaming, we can't easily change HTTP status code after it starts, 
            # but we can yield an error message chunk or handle it gracefully.
            yield f"\n[Error: {str(e)}]"

    return StreamingResponse(event_generator(), media_type="text/plain")
