from .session import fetch_one


def insert_message(
    conversation_id: str,
    direction: str,
    content: str,
    whatsapp_message_id: str = None,
):
    stmt = """
        INSERT INTO messages (
            conversation_id,
            direction,
            content,
            whatsapp_message_id
        )
        VALUES (
            :conversation_id,
            :direction,
            :content,
            :whatsapp_message_id
        )
        RETURNING *
    """

    return fetch_one(stmt, {
        "conversation_id": conversation_id,
        "direction": direction,
        "content": content,
        "whatsapp_message_id": whatsapp_message_id,
    })