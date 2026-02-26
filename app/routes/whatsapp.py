# app/routes/whatsapp.py

import os
from fastapi import APIRouter, Request, HTTPException
from app.services.whatsapp_service import process_whatsapp_message

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def receive_message(request: Request):
    payload = await request.json()

    try:
        await process_whatsapp_message(payload)
    except Exception as e:
        # Log error properly in production
        print("Webhook processing error:", e)

    return {"status": "ok"}