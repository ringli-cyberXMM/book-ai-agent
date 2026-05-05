from app.services.recommend_service import recommend_books
from app.services.ai_service import ask_ai

def get_reply(user_id: str, message: str):
    if "book" in message.lower():
        books = recommend_books(message)
        return f"Recommended books: {', '.join(books)}"
    
    return ask_ai(user_id,message)