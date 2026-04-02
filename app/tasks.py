import time
from celery.exceptions import MaxRetriesExceededError

from app.celery_app import celery
from app.ai.service import classify_lead

from app.db.leads import (
    update_lead_ai,
    get_lead_ai_status,
    update_lead_ai_status,
    get_lead_by_id,
)
from app.db.ai_logs import insert_ai_log

from app.services.email_sender import send_email


@celery.task(
    name="app.tasks.process_ai_for_lead",
    bind=True,
    max_retries=5,
)
def process_ai_for_lead(self, lead_id: str, message: str, metadata: dict = None):
    try:
        update_lead_ai_status(lead_id, "PROCESSING")

        existing = get_lead_ai_status(lead_id)
        if existing and existing.get("ai_summary"):
            update_lead_ai_status(lead_id, "COMPLETED")
            return "Already processed"

        start_time = time.time()
        result = classify_lead(message, lead_id=None)
        latency_ms = int((time.time() - start_time) * 1000)

        insert_ai_log(
            lead_id=lead_id,
            provider="openrouter",
            model="configured-model",
            prompt="handled inside provider",
            raw_response=str(result),
            latency_ms=latency_ms,
        )

        update_lead_ai(
            lead_id=lead_id,
            summary=result.get("summary"),
            intent=result.get("intent"),
            followup=result.get("followup"),
        )

        update_lead_ai_status(lead_id, "COMPLETED")

        _handle_email_response(lead_id, result, metadata or {})

        return "Completed"

    except Exception as exc:
        return _handle_retry(self, lead_id, exc)


def _handle_email_response(lead_id: str, result: dict, metadata: dict):
    try:
        lead = get_lead_by_id(lead_id)

        if not lead or lead.get("source") != "email":
            return

        recipient = lead.get("phone_number")
        followup = result.get("followup")

        if not recipient or not followup:
            return

        subject = metadata.get("subject", "Your inquiry")
        message_id = metadata.get("message_id")

        send_email(
            to_email=recipient,
            message=followup,
            subject=subject,
            message_id=message_id,
        )

    except Exception as e:
        print(f"[EmailResponse] Failed for lead {lead_id}: {e}")


def _handle_retry(task, lead_id: str, exc: Exception):
    try:
        raise task.retry(
            exc=exc,
            countdown=2 ** task.request.retries,
        )

    except MaxRetriesExceededError:
        update_lead_ai_status(lead_id, "FAILED")

        insert_ai_log(
            lead_id=lead_id,
            provider="system",
            model="retry_handler",
            prompt="final_failure",
            raw_response=str(exc),
            latency_ms=0,
        )

        raise