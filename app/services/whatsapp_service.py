from app.db.organizations import get_organization_by_phone_number_id
from app.db.leads import create_lead
from app.db.lead_details import insert_lead_details

from app.tasks import process_ai_for_lead


async def process_internal_message(
    user_id: str,
    message: str,
    channel: str = "whatsapp",
    organization_id: str = None,
    metadata: dict = None,
):
    """
    Entry point for all incoming messages (email, WhatsApp, etc.).
    Responsible for creating leads and dispatching AI processing.
    """

    if organization_id:
        org = {"id": organization_id, "name": "ExternalClient"}
    else:
        phone_number_id = "test-number-001"
        org = get_organization_by_phone_number_id(phone_number_id)

    if not org:
        return {"error": "Organization not found"}

    lead = create_lead(
        organization_id=org["id"],
        contact_name="Unknown",
        phone_number=user_id,
        source=channel,
    )

    insert_lead_details(
        lead_id=lead["id"],
        data={
            "raw_message": message,
            "metadata": metadata or {},
        },
    )

    process_ai_for_lead.delay(
        lead["id"],
        message,
        metadata or {},
    )

    return {
        "lead_id": lead["id"],
        "organization": org["name"],
        "status": "queued_for_processing",
    }
    
async def process_whatsapp_message(payload: dict):
    """
    Temporary compatibility layer for WhatsApp route.
    Keeps existing routes functional while system becomes channel-agnostic.
    """

    try:
        # Extract fields (adjust later for real webhook)
        sender = payload.get("phone_number")
        message = payload.get("message")

        if not sender or not message:
            return {"error": "Invalid payload"}

        return await process_internal_message(
            user_id=sender,
            message=message,
            channel="whatsapp",
        )

    except Exception as e:
        print(f"[WhatsAppService] Error: {e}")
        return {"error": "processing_failed"}