def detect_language(text: str):
    for ch in text:
        if '\u1000' <= ch <= '\u109F':
            return "mm"
        elif '\u3040' <= ch <= 'u30FF':
            return "jp"
    return "en"