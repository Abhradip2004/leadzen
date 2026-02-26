from fastapi import BackgroundTasks
from app.db.organizations import get_organization_by_phone_number_id
from app.db.leads import create_lead, update_lead_ai
from app.db.lead_details import insert_lead_details
from app.ai.service import classify_lead

from app.db.webhook_events import (
    insert_webhook_event,
    mark_webhook_processed,
    mark_webhook_failed,
)
from app.db.conversations import create_conversation
from app.db.messages import insert_message


def process_ai_for_lead(lead_id: str, message: str):
    ai_result = classify_lead(message, lead_id)

    update_lead_ai(
        lead_id=lead_id,
        summary=ai_result["summary"],
        intent=ai_result["intent"],
        followup=ai_result["followup"],
    )

async def process_whatsapp_message(payload: dict, background_tasks):
    """
    Placeholder webhook processor.
    """

    # TODO: Extract phone_number_id from payload properly
    phone_number_id = "test-number-001"

    # TODO: Extract sender + message properly
    phone_number = "unknown"
    message = "unknown"

    return await process_internal_message(
        phone_number=phone_number,
        message=message,
        background_tasks=background_tasks
    )

async def process_internal_message(
    phone_number: str,
    message: str,
    background_tasks: BackgroundTasks,
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

    # Example dynamic extraction (temporary placeholder)
    extracted_details = {
        "raw_message": message
    }

    insert_lead_details(lead["id"], extracted_details)

    background_tasks.add_task(
        process_ai_for_lead,
        lead["id"],
        message
    )

    return {
        "lead_id": lead["id"],
        "organization": org["name"],
        "status": "processing",
    }
    

async def process_whatsapp_message(payload: dict, background_tasks):
    """
    Full traceable webhook pipeline.
    """

    # Extract unique event id (you'll replace with real Meta field later)
    event_id = payload.get("event_id", "test-event")

    # Store raw event
    event = insert_webhook_event(event_id, payload)

    # If duplicate event, skip
    if event is None:
        return {"status": "duplicate_event"}

    try:
        # Extract fields properly later
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

        background_tasks.add_task(
            process_ai_for_lead,
            lead["id"],
            message_text,
        )

        mark_webhook_processed(event["id"])

        return {"status": "processed"}

    except Exception as e:
        mark_webhook_failed(event["id"], str(e))
        raise