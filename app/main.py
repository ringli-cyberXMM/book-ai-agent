from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.webhook.facebook import router as facebook_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(facebook_router)


@app.get("/")
def home():
    return {"message": "Book AI Agent is running"}