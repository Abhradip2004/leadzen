from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection, release_connection


def create_lead(
    organization_id: str,
    contact_name: str,
    phone_number: str,
    source: str = "whatsapp",
    webhook_event_id: str = None,
):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO leads (
                    organization_id,
                    contact_name,
                    phone_number,
                    source,
                    webhook_event_id
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    organization_id,
                    contact_name,
                    phone_number,
                    source,
                    webhook_event_id,
                ),
            )

            conn.commit()
            return cur.fetchone()

    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)


def update_lead_ai(
    lead_id: str,
    summary: str,
    intent: str,
    followup: str,
):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE leads
                SET
                    ai_summary = %s,
                    ai_intent = %s,
                    ai_followup = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                (summary, intent, followup, lead_id),
            )

            conn.commit()
            return cur.fetchone()

    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)