from psycopg2.extras import RealDictCursor
from app.db.connection import get_connection, release_connection


def get_organization_by_phone_number_id(phone_number_id: str):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM organizations
                WHERE whatsapp_phone_number_id = %s
                LIMIT 1
                """,
                (phone_number_id,),
            )
            return cur.fetchone()
    finally:
        release_connection(conn)