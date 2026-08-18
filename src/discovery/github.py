import requests


GITHUB_API_URL = "https://api.github.com/search/repositories"


def search_github_repositories(
    query: str,
    limit: int = 20,
) -> list[dict]:
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }

    response = requests.get(
        GITHUB_API_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("items", [])