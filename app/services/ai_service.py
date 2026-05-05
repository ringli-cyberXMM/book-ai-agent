import os
from openai import OpenAI
from app.utils.language import detect_language
from app.services.memory import get_history, save_message

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(user_id: str, message: str):
    lang = detect_language(message)

    if lang == "mm":
        system_prompt = "You are a helpful assistant. Reply in Myanmar language."
    elif lang == "jp":
        system_prompt = "You are a helpful assistant. Reply in Japanese."
    else:
        system_prompt = "You are a helpful assistant. Reply in English."


    history = get_history(user_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model = "gpt-5-mini",
        messages=messages
    )


    reply =  response.choices[0].message.content

    #save conversation
    save_message(user_id, "user", message)
    save_message(user_id, "assistant", reply)

    return reply