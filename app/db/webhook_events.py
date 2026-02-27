from .session import fetch_one, execute
import json


def insert_webhook_event(event_id: str, payload: dict):
    stmt = """
        INSERT INTO webhook_events (event_id, payload)
        VALUES (:event_id, :payload)
        ON CONFLICT (event_id) DO NOTHING
        RETURNING *
    """

    return fetch_one(stmt, {
        "event_id": event_id,
        "payload": json.dumps(payload),
    })


def mark_webhook_processed(event_db_id: str):
    stmt = """
        UPDATE webhook_events
        SET processed = TRUE,
            processed_at = NOW()
        WHERE id = :event_db_id
    """

    execute(stmt, {"event_db_id": event_db_id})


def mark_webhook_failed(event_db_id: str, error: str):
    stmt = """
        UPDATE webhook_events
        SET processed = FALSE,
            processing_error = :error,
            processed_at = NOW()
        WHERE id = :event_db_id
    """

    execute(stmt, {
        "event_db_id": event_db_id,
        "error": error,
    })