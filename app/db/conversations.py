from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection, release_connection


def create_conversation(lead_id: str, organization_id: str):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO conversations (
                    lead_id,
                    organization_id
                )
                VALUES (%s, %s)
                RETURNING *
                """,
                (lead_id, organization_id),
            )
            conn.commit()
            return cur.fetchone()
    finally:
        release_connection(conn)