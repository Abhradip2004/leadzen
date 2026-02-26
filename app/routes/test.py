from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.services.whatsapp_service import process_internal_message

router = APIRouter()


class TestMessage(BaseModel):
    phone_number: str
    message: str


@router.post("/test-message")
async def test_message(data: TestMessage, background_tasks: BackgroundTasks):
    result = await process_internal_message(
        phone_number=data.phone_number,
        message=data.message,
        background_tasks=background_tasks
    )

    return result