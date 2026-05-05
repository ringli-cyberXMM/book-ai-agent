import html

def sanitize_input(text: str):
    return html.escape(text)