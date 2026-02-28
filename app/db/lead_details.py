from .session import fetch_one
import json


def insert_lead_details(lead_id: str, data: dict):
    stmt = """
        INSERT INTO lead_details (
            lead_id,
            data
        )
        VALUES (
            :lead_id,
            :data
        )
        RETURNING *
    """

    return fetch_one(stmt, {
        "lead_id": lead_id,
        "data": json.dumps(data),
    })

def get_lead_raw_message(lead_id: str):
    stmt = """
        SELECT data
        FROM lead_details
        WHERE lead_id = :lead_id
        ORDER BY created_at ASC
        LIMIT 1
    """
    result = fetch_one(stmt, {"lead_id": lead_id})

    if not result:
        return None

    return result["data"].get("raw_message")