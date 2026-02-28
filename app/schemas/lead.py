from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadResponse(BaseModel):
    id: str
    contact_name: Optional[str]
    phone_number: str
    source: Optional[str]
    ai_summary: Optional[str]
    ai_intent: Optional[str]
    ai_followup: Optional[str]
    ai_status: str
    created_at: datetime


class LeadListResponse(BaseModel):
    leads: list[LeadResponse]
    total: int

class SingleLeadResponse(BaseModel):
    lead: LeadResponse