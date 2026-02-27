from app.db.organizations import get_organization_by_phone_number_id
from app.db.leads import create_lead
from app.db.lead_details import insert_lead_details
from app.db.webhook_events import (
    insert_webhook_event,
    mark_webhook_processed,
    mark_webhook_failed,
)
from app.db.conversations import create_conversation
from app.db.messages import insert_message

from app.tasks import process_ai_for_lead


# ------------------------------------------------------------------
# Internal Message Processing (used by test endpoint)
# ------------------------------------------------------------------

async def process_internal_message(
    phone_number: str,
    message: str,
):
    phone_number_id = "test-number-001"

    org = get_organization_by_phone_number_id(phone_number_id)

    if not org:
        return {"error": "Organization not found"}

    lead = create_lead(
        organization_id=org["id"],
        contact_name="Unknown",
        phone_number=phone_number,
        source="whatsapp",
    )

    insert_lead_details(
        lead_id=lead["id"],
        data={"raw_message": message},
    )

    # 🚀 Dispatch Celery task
    process_ai_for_lead.delay(
        lead["id"],
        message,
    )

    return {
        "lead_id": lead["id"],
        "organization": org["name"],
        "status": "queued_for_processing",
    }


# ------------------------------------------------------------------
# Full Webhook Processing (Production Path)
# ------------------------------------------------------------------

async def process_whatsapp_message(payload: dict):
    """
    Full traceable webhook pipeline.
    """

    # Unique event ID (replace with real Meta field later)
    event_id = payload.get("event_id", "test-event")

    # Store raw webhook event
    event = insert_webhook_event(event_id, payload)

    # Duplicate event guard
    if event is None:
        return {"status": "duplicate_event"}

    try:
        # TODO: Replace with real extraction
        phone_number_id = "test-number-001"
        sender_number = payload.get("phone_number")
        message_text = payload.get("message")

        org = get_organization_by_phone_number_id(phone_number_id)

        if not org:
            raise Exception("Organization not found")

        lead = create_lead(
            organization_id=org["id"],
            contact_name="Unknown",
            phone_number=sender_number,
            source="whatsapp",
            webhook_event_id=event["id"],
        )

        conversation = create_conversation(
            lead_id=lead["id"],
            organization_id=org["id"],
        )

        insert_message(
            conversation_id=conversation["id"],
            direction="incoming",
            content=message_text,
        )

        # 🚀 Dispatch Celery task
        process_ai_for_lead.delay(
            lead["id"],
            message_text,
        )

        mark_webhook_processed(event["id"])

        return {"status": "processed"}

    except Exception as e:
        mark_webhook_failed(event["id"], str(e))
        raise