memory_store = {}

def get_history(user_id: str):
    return memory_store.get(user_id, [])

def save_message(user_id: str, role: str, content: str):
    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append({
        "role": role,
        "content": content
    })

    #limit memory(last 10 messages)
    memory_store[user_id] = memory_store[user_id][-10:]