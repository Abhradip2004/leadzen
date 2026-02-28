import time
from celery.exceptions import MaxRetriesExceededError
from app.celery_app import celery
from app.ai.service import classify_lead
from app.db.leads import (
    update_lead_ai,
    get_lead_ai_status,
    update_lead_ai_status,
)
from app.db.ai_logs import insert_ai_log


@celery.task(
    name="app.tasks.process_ai_for_lead",
    bind=True,
    max_retries=5,
)
def process_ai_for_lead(self, lead_id: str, message: str):

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
            summary=result["summary"],
            intent=result["intent"],
            followup=result["followup"],
        )

        update_lead_ai_status(lead_id, "COMPLETED")

        return "Completed"

    except Exception as exc:
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
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