import requests


HUGGING_FACE_SPACES_URL = "https://huggingface.co/api/spaces"


def search_ai_tools(
    limit: int = 20,
) -> list[dict]:
    params = {
        "limit": limit,
        "sort": "likes",
        "direction": -1,
    }

    response = requests.get(
        HUGGING_FACE_SPACES_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    spaces = response.json()

    return spaces[:limit]