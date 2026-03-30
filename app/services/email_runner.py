import asyncio
from app.services.email_service import EmailService


async def run_email_listener():
    service = EmailService()

    while True:
        await service.check_all_inboxes()
        await asyncio.sleep(30)