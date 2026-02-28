from fastapi import APIRouter, Query, HTTPException
from app.db.leads import (
    get_all_leads,
    get_total_leads_count,
    get_lead_details,
)
from app.schemas.lead import LeadListResponse, SingleLeadResponse

from app.db.conversations import get_conversations_by_lead_id
from app.schemas.conversation import ConversationListResponse


router = APIRouter(prefix="/api/v1/leads", tags=["v1-leads"])


@router.get("", response_model=LeadListResponse)
def list_leads(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    ai_status: str | None = Query(None),
    search: str | None = Query(None),
):
    leads = get_all_leads(
        limit=limit,
        offset=offset,
        ai_status=ai_status,
        search=search,
    )

    total = get_total_leads_count(
        ai_status=ai_status,
        search=search,
    )

    return {
        "leads": leads,
        "total": total,
    }


@router.get("/{lead_id}", response_model=SingleLeadResponse)
def get_lead(lead_id: str):
    lead = get_lead_details(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {"lead": lead}

@router.get("/{lead_id}/conversations", response_model=ConversationListResponse)
def get_lead_conversations(lead_id: str):
    conversations = get_conversations_by_lead_id(lead_id)

    return {"conversations": conversations}