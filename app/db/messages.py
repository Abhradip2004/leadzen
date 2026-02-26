from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection, release_connection


def insert_message(
    conversation_id: str,
    direction: str,
    content: str,
    whatsapp_message_id: str = None,
):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO messages (
                    conversation_id,
                    direction,
                    content,
                    whatsapp_message_id
                )
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                (conversation_id, direction, content, whatsapp_message_id),
            )
            conn.commit()
            return cur.fetchone()
    finally:
        release_connection(conn)