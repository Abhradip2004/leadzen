from .session import fetch_one


def get_organization_by_phone_number_id(phone_number_id: str):
    stmt = """
        SELECT *
        FROM organizations
        WHERE whatsapp_phone_number_id = :phone_number_id
        LIMIT 1
    """

    return fetch_one(stmt, {
        "phone_number_id": phone_number_id
    })