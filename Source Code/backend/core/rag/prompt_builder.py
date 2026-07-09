import logging
from typing import Dict, Any, List
from ...config.settings import settings

logger = logging.getLogger(__name__)

class PromptBuilder:
    def __init__(self):
        self.max_size = settings.MAX_PROMPT_AUGMENTATION_SIZE

    def build_messages(self, user_prompt: str, context: Dict[str, Any]) -> List[Dict[str, str]]:
        messages = []
        
        # 1. System Prompt
        system_content = "You are LUFFY AI."
        
        # 2. Pinned Memory
        if context.get("pinned"):
            system_content += "\\nPinned Rules:\\n" + "\\n".join(context["pinned"])
            
        # 3. Conversation Summary
        if context.get("summary"):
            system_content += f"\\nSummary:\\n{context['summary']}"
            
        messages.append({"role": "system", "content": system_content})

        # 4. Short Memory
        for msg in context.get("short_memory", []):
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            
        # 5 & 6. Retrieved Long Memory & Knowledge
        retrieved_texts = []
        for mem in context.get("long_memory", []):
            retrieved_texts.append(mem.get("content", ""))
            
        context_str = "\\n".join(retrieved_texts)
        if len(context_str) > self.max_size:
            context_str = context_str[:self.max_size] + "..." # Size Protection
            
        final_user_prompt = user_prompt
        if context_str:
            final_user_prompt = f"Relevant Context:\\n{context_str}\\n\\nUser Query:\\n{user_prompt}"

        # 7. Current User Prompt
        messages.append({"role": "user", "content": final_user_prompt})
        
        return messages
