from fastapi import APIRouter
from app.tasks import process_ai_for_lead
from app.db.leads import get_lead_by_id, update_lead_ai_status

from app.db.lead_details import get_lead_raw_message

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/retry-ai/{lead_id}")
def retry_ai(lead_id: str):

    lead = get_lead_by_id(lead_id)

    if not lead:
        return {"error": "Lead not found"}

    from app.db.lead_details import get_lead_raw_message

    message = get_lead_raw_message(lead_id)

    if not message:
        return {"error": "No stored message found for this lead"}

    update_lead_ai_status(lead_id, "PENDING")

    process_ai_for_lead.delay(lead_id, message)

    return {"status": "requeued"}