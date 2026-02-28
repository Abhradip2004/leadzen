from .session import fetch_one, fetch_all, execute


def create_lead(
    organization_id: str,
    contact_name: str,
    phone_number: str,
    source: str = "whatsapp",
    webhook_event_id: str = None,
):
    stmt = """
        INSERT INTO leads (
            organization_id,
            contact_name,
            phone_number,
            source,
            webhook_event_id
        )
        VALUES (
            :organization_id,
            :contact_name,
            :phone_number,
            :source,
            :webhook_event_id
        )
        RETURNING *
    """

    return fetch_one(stmt, {
        "organization_id": organization_id,
        "contact_name": contact_name,
        "phone_number": phone_number,
        "source": source,
        "webhook_event_id": webhook_event_id,
    })


def update_lead_ai(
    lead_id: str,
    summary: str,
    intent: str,
    followup: str,
):
    stmt = """
        UPDATE leads
        SET
            ai_summary = :summary,
            ai_intent = :intent,
            ai_followup = :followup,
            updated_at = NOW()
        WHERE id = :lead_id
        RETURNING *
    """

    return fetch_one(stmt, {
        "summary": summary,
        "intent": intent,
        "followup": followup,
        "lead_id": lead_id,
    })


def get_lead_ai_status(lead_id: str):
    stmt = """
        SELECT ai_summary, ai_status
        FROM leads
        WHERE id = :lead_id
    """
    
    return fetch_one(stmt, {"lead_id": lead_id})


def update_lead_ai_status(lead_id: str, status: str):
    stmt = """
        UPDATE leads
        SET
            ai_status = :status,
            updated_at = NOW()
        WHERE id = :lead_id
        RETURNING *
    """

    return fetch_one(stmt, {
        "status": status,
        "lead_id": lead_id,
    })


def get_lead_by_id(lead_id: str):
    stmt = """
        SELECT *
        FROM leads
        WHERE id = :lead_id
    """

    return fetch_one(stmt, {"lead_id": lead_id})

def get_all_leads(limit: int = 50, offset: int = 0):
    stmt = """
        SELECT *
        FROM leads
        ORDER BY created_at DESC
        LIMIT :limit
        OFFSET :offset
    """
    return fetch_all(stmt, {
        "limit": limit,
        "offset": offset,
    })


def get_total_leads_count():
    stmt = "SELECT COUNT(*) as count FROM leads"
    result = fetch_one(stmt)
    return result["count"]

def get_lead_details(lead_id: str):
    stmt = """
        SELECT *
        FROM leads
        WHERE id = :lead_id
    """
    return fetch_one(stmt, {"lead_id": lead_id})