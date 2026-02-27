from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.engine import Result
from .engine import engine


@contextmanager
def get_db():
    """
    Provides transactional scope.
    Auto commit / rollback.
    """
    connection = engine.connect()
    transaction = connection.begin()
    try:
        yield connection
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        connection.close()


def fetch_one(stmt: str, params: dict = None):
    with get_db() as conn:
        result: Result = conn.execute(text(stmt), params or {})
        row = result.mappings().first()
        return dict(row) if row else None


def fetch_all(stmt: str, params: dict = None):
    with get_db() as conn:
        result: Result = conn.execute(text(stmt), params or {})
        rows = result.mappings().all()
        return [dict(r) for r in rows]


def execute(stmt: str, params: dict = None):
    with get_db() as conn:
        conn.execute(text(stmt), params or {})