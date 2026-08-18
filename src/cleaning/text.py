import re
from html import unescape


def clean_text(text: str | None) -> str:
    if not text:
        return ""

    text = unescape(text)

    # Remove Markdown links but keep the visible text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()