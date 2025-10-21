def safe_truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    short = text[:max_chars]
    if " " in short:
        short = short.rsplit(" ", 1)[0]
    return short
