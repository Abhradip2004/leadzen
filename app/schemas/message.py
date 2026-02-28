from pydantic import BaseModel
from datetime import datetime
from typing import List


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    direction: str
    content: str
    created_at: datetime


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]