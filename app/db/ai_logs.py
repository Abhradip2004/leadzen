from .session import fetch_one


def insert_ai_log(
    lead_id: str,
    provider: str,
    model: str,
    prompt: str,
    raw_response: str,
    latency_ms: int,
):
    stmt = """
        INSERT INTO ai_logs (
            lead_id,
            provider,
            model,
            prompt,
            raw_response,
            latency_ms
        )
        VALUES (
            :lead_id,
            :provider,
            :model,
            :prompt,
            :raw_response,
            :latency_ms
        )
        RETURNING *
    """

    return fetch_one(stmt, {
        "lead_id": lead_id,
        "provider": provider,
        "model": model,
        "prompt": prompt,
        "raw_response": raw_response,
        "latency_ms": latency_ms,
    })