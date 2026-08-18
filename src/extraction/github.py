from src.classification.entity import classify_entity
from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def repository_to_entity(repository: dict) -> Entity:
    repository_url = normalize_url(repository.get("html_url"))

    owner = repository.get("owner", {})
    license_info = repository.get("license") or {}

    name = clean_text(repository.get("name"))
    description = clean_text(repository.get("description"))

    entity_type = classify_entity(
        name=name,
        description=description,
        source_type="GitHub",
    )

    return Entity(
        id=f"github-{repository['id']}",
        entity_type=entity_type,
        name=name,
        description=description,
        url=repository_url,
        categories=["AI", "Open Source"],
        source=Source(
            name="GitHub",
            url=repository_url,
        ),
        metadata={
            "stars": repository.get("stargazers_count", 0),
            "forks": repository.get("forks_count", 0),
            "primary_language": repository.get("language"),
            "last_updated": repository.get("updated_at"),
            "created_at": repository.get("created_at"),
            "owner": clean_text(owner.get("login")),
            "license": license_info.get("spdx_id"),
        },
    )


def repositories_to_entities(
    repositories: list[dict],
) -> list[Entity]:
    return [
        repository_to_entity(repository)
        for repository in repositories
    ]