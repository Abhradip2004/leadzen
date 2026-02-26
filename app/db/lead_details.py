from psycopg2.extras import RealDictCursor, Json
from app.db.connection import get_connection, release_connection


def insert_lead_details(lead_id: str, data: dict):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO lead_details (lead_id, data)
                VALUES (%s, %s)
                RETURNING *
                """,
                (lead_id, Json(data)),
            )

            conn.commit()
            return cur.fetchone()

    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)