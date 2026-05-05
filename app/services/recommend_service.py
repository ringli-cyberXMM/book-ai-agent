import json

def recommend_books(topic: str):
    with open("app/db/books.json", "r", encoding="utf-8") as f:
        books = json.load(f)

    result = []

    for book in books:
        if topic.lower() in book["category"]:
            result.append(book["title"])

    return result if result else ["No book found"]