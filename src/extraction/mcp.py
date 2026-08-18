from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def mcp_to_entity(repository: dict) -> Entity:
    repository_url = normalize_url(
        repository.get("html_url")
    )

    owner = repository.get("owner", {})

    return Entity(
        id=f"mcp-{repository['id']}",
        entity_type="mcp_server",
        name=clean_text(
            repository.get("name")
        ),
        description=clean_text(
            repository.get("description")
        ),
        url=repository_url,
        categories=[
            "AI",
            "MCP",
            "Open Source",
        ],
        source=Source(
            name="GitHub",
            url=repository_url,
        ),
        metadata={
            "stars": repository.get(
                "stargazers_count",
                0,
            ),
            "forks": repository.get(
                "forks_count",
                0,
            ),
            "owner": clean_text(
                owner.get("login")
            ),
            "language": repository.get(
                "language"
            ),
            "last_updated": repository.get(
                "updated_at"
            ),
            "license": (
                repository.get("license") or {}
            ).get("spdx_id"),
        },
    )


def mcp_servers_to_entities(
    repositories: list[dict],
) -> list[Entity]:
    return [
        mcp_to_entity(repository)
        for repository in repositories
    ]