from fastapi import APIRouter, HTTPException
from app.db.messages import get_messages_by_conversation_id
from app.schemas.message import MessageListResponse

router = APIRouter(prefix="/api/v1/conversations", tags=["v1-conversations"])


@router.get("/{conversation_id}/messages", response_model=MessageListResponse)
def get_conversation_messages(conversation_id: str):
    messages = get_messages_by_conversation_id(conversation_id)

    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"messages": messages}