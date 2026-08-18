import requests


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


MCP_QUERIES = [
    "MCP server",
    "model context protocol",
    "mcp-server",
]


def search_mcp_servers(
    limit: int = 30,
) -> list[dict]:
    repositories = []
    seen_ids = set()

    per_query = max(10, limit // len(MCP_QUERIES))

    for query in MCP_QUERIES:
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_query,
        }

        response = requests.get(
            GITHUB_SEARCH_URL,
            params=params,
            timeout=15,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "AI-Orbit-Ingestion/1.0",
            },
        )

        response.raise_for_status()

        data = response.json()

        for repository in data.get("items", []):
            repository_id = repository.get("id")

            if repository_id in seen_ids:
                continue

            seen_ids.add(repository_id)
            repositories.append(repository)

            if len(repositories) >= limit:
                return repositories

    return repositories