from pydantic import BaseModel
from datetime import datetime
from typing import List


class ConversationResponse(BaseModel):
    id: str
    lead_id: str
    organization_id: str
    created_at: datetime


class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]   