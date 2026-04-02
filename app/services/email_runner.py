import asyncio
from app.services.email_service import EmailService


POLL_INTERVAL_SECONDS = 30


async def run_email_listener():
    """
    Background task to continuously poll email inboxes.
    Designed to be resilient and non-blocking.
    """

    service = EmailService()

    while True:
        try:
            await service.check_all_inboxes()
        except Exception as e:
            print(f"[EmailRunner] Unexpected error: {e}")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)