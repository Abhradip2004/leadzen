from .session import fetch_one


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