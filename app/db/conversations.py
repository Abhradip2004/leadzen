from .session import fetch_one, fetch_all


def create_conversation(lead_id: str, organization_id: str):
    stmt = """
        INSERT INTO conversations (
            lead_id,
            organization_id
        )
        VALUES (
            :lead_id,
            :organization_id
        )
        RETURNING *
    """

    return fetch_one(stmt, {
        "lead_id": lead_id,
        "organization_id": organization_id,
    })

def get_conversations_by_lead_id(lead_id: str):
    stmt = """
        SELECT *
        FROM conversations
        WHERE lead_id = :lead_id
        ORDER BY created_at ASC
    """
    return fetch_all(stmt, {"lead_id": lead_id})