from urllib.parse import urlparse, urlunparse


def normalize_url(url: str | None) -> str:
    if not url:
        return ""

    url = str(url).strip()

    # If this is a Markdown link, use the destination URL.
    if "](" in url:
        url = url.split("](", 1)[1]

    # Remove Markdown closing parenthesis.
    url = url.rstrip(")")

    # Remove accidental backslashes.
    url = url.replace("\\", "").strip()

    # If multiple URLs are present, use the last HTTP/HTTPS URL.
    https_position = url.rfind("https://")
    http_position = url.rfind("http://")

    position = max(https_position, http_position)

    if position >= 0:
        url = url[position:]

    parsed = urlparse(url)

    if not parsed.scheme:
        parsed = urlparse(f"https://{url}")

    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            parsed.query,
            "",
        )
    )