from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user, assistant, system)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="List of previous messages in the conversation")
    model: Optional[str] = Field(None, description="Optional override for the model to use")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
