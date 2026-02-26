from psycopg2.extras import RealDictCursor, Json
from app.db.connection import get_connection, release_connection


def insert_webhook_event(event_id: str, payload: dict):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO webhook_events (event_id, payload)
                VALUES (%s, %s)
                ON CONFLICT (event_id) DO NOTHING
                RETURNING *
                """,
                (event_id, Json(payload)),
            )
            conn.commit()
            return cur.fetchone()
    finally:
        release_connection(conn)


def mark_webhook_processed(event_db_id: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE webhook_events
                SET processed = TRUE,
                    processed_at = NOW()
                WHERE id = %s
                """,
                (event_db_id,),
            )
            conn.commit()
    finally:
        release_connection(conn)


def mark_webhook_failed(event_db_id: str, error: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE webhook_events
                SET processed = FALSE,
                    processing_error = %s,
                    processed_at = NOW()
                WHERE id = %s
                """,
                (error, event_db_id),
            )
            conn.commit()
    finally:
        release_connection(conn)