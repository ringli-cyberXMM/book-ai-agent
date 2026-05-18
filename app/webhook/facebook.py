from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
import requests
import os

from app.services.chatbot_service import get_reply

router = APIRouter()

VERIFY_TOKEN = "myverify123"
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")


@router.get("/webhook/facebook")
def verify(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)

    return PlainTextResponse(
        content="Verification failed",
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