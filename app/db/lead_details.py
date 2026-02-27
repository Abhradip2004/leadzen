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