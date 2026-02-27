from fastapi import APIRouter
from pydantic import BaseModel
from app.services.whatsapp_service import process_internal_message

router = APIRouter()


class TestMessage(BaseModel):
    phone_number: str
    message: str


@router.post("/test-message")
async def test_message(data: TestMessage):
    return await process_internal_message(
        phone_number=data.phone_number,
        message=data.message,
    )