from typing import AsyncGenerator, List, Dict
from core.intent_engine import intent_engine
from core.provider_engine import provider_engine

class ReasoningEngine:
    """
    Manages complex, multi-step tasks. Decides when to break down a request
    and coordinates the sequence of actions. In Phase 3, this handles standard chat routing.
    """
    async def process_request(self, messages: List[Dict[str, str]], model: str = None) -> AsyncGenerator[str, None]:
        # Step 1: Analyze intent
        intent = await intent_engine.analyze(messages)
        
        # Step 2: Coordinate flow based on intent
        if intent == "chat":
            # Stream directly from Provider Engine
            async for chunk in provider_engine.stream_chat(messages, model):
                yield chunk
        else:
            # Fallback for future intents
            yield "Sorry, I can only process standard chat messages at this time."

reasoning_engine = ReasoningEngine()
