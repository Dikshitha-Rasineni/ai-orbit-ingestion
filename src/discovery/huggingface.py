import requests


HUGGING_FACE_MODELS_URL = "https://huggingface.co/api/models"


def search_huggingface_models(
    search: str = "",
    limit: int = 20,
) -> list[dict]:
    params = {
        "search": search,
        "limit": limit,
        "sort": "downloads",
        "direction": -1,
    }

    response = requests.get(
        HUGGING_FACE_MODELS_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()