from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
import requests
import os

from app.services.chatbot_service import get_reply

router = APIRouter()

VERIFY_TOKEN = "myverify123"
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")


@router.get("/webhook/facebook")
async def verify(request: Request):

    hub_verify_token = request.query_params.get("hub.verify_token")
    hub_challenge = request.query_params.get("hub.challenge")

    if hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )

@router.post("/webhook/facebook")
async def webhook(request: Request):
    data = await request.json()

    for entry in data.get("entry", []):
        for messaging in entry.get("messaging", []):

            sender_id = messaging["sender"]["id"]

            if "message" in messaging:

                text = messaging["message"].get("text")

                if text:
                    reply = get_reply(sender_id, text)
                    send_message(sender_id, reply)

    return {"status": "ok"}


def send_message(user_id, text):

    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={FB_PAGE_TOKEN}"

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload)