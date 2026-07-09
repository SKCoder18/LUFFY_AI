from typing import List, Dict

class IntentEngine:
    """
    Analyzes user input to determine the goal (e.g., casual chat, tool execution, memory retrieval).
    In Phase 3, this is a baseline stub that routes everything as 'chat'.
    """
    async def analyze(self, messages: List[Dict[str, str]]) -> str:
        # Phase 3 scope: standard text chat only
        return "chat"

intent_engine = IntentEngine()
