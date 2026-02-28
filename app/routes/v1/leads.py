from fastapi import APIRouter, Query, HTTPException
from app.db.leads import (
    get_all_leads,
    get_total_leads_count,
    get_lead_details,
)
from app.schemas.lead import LeadListResponse, SingleLeadResponse

router = APIRouter(prefix="/api/v1/leads", tags=["v1-leads"])


@router.get("", response_model=LeadListResponse)
def list_leads(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    leads = get_all_leads(limit=limit, offset=offset)
    total = get_total_leads_count()

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