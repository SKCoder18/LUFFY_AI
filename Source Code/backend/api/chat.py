import time
import json
import logging
import httpx
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.core.rag.prompt_builder import PromptBuilder
from backend.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks, req: Request):
    start_time = time.time()
    
    # Retrieve App state components
    memory_manager = req.app.state.memory_manager
    prompt_builder = PromptBuilder()
    
    # 1. Retrieve Context
    retrieval_start = time.time()
    context = await memory_manager.get_context(request.conversation_id, request.message)
    retrieval_time = time.time() - retrieval_start
    
    # 2. Build Prompt
    build_start = time.time()
    messages = prompt_builder.build_messages(request.message, context)
    build_time = time.time() - build_start
    
    logger.info(f"Retrieved Context in {retrieval_time*1000:.2f}ms. Built Prompt in {build_time*1000:.2f}ms.")
    
    async def stream_generator():
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": settings.DEFAULT_MODEL,
            "messages": messages,
            "stream": True
        }
        
        full_response = ""
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, json=payload, timeout=settings.OLLAMA_TIMEOUT) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_lines():
                        if chunk:
                            try:
                                data = json.loads(chunk)
                                if "message" in data and "content" in data["message"]:
                                    content = data["message"]["content"]
                                    full_response += content
                                    yield content
                            except json.JSONDecodeError:
                                pass
                                
            # Non-blocking Background Task: Save interaction & Extract Memory
            background_tasks.add_task(
                memory_manager.save_interaction, 
                request.conversation_id, 
                request.message, 
                full_response
            )
            
            pipeline_time = time.time() - start_time
            logger.info(f"Total Pipeline Time: {pipeline_time*1000:.2f}ms")
            
        except httpx.RequestError as e:
            logger.error(f"Error communicating with Ollama: {str(e)}")
            yield f"\\n\\n[Error communicating with Ollama: {str(e)}]"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
