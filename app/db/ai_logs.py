import time
from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection, release_connection


def insert_ai_log(
    lead_id: str,
    provider: str,
    model: str,
    prompt: str,
    raw_response: str,
    latency_ms: int,
):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                INSERT INTO ai_logs (
                    lead_id,
                    provider,
                    model,
                    prompt,
                    raw_response,
                    latency_ms
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
            """

            cur.execute(
                query,
                (
                    lead_id,
                    provider,
                    model,
                    prompt,
                    raw_response,
                    latency_ms,
                ),
            )

            conn.commit()
            return cur.fetchone()

    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)