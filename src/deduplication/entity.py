import re

from rapidfuzz.fuzz import ratio

from src.models import Entity


def normalize_name(name: str) -> str:
    name = name.lower().strip()

    name = re.sub(
        r"[^a-z0-9\s]",
        "",
        name,
    )

    name = re.sub(
        r"\s+",
        " ",
        name,
    )

    return name


def names_are_similar(
    first: str,
    second: str,
    threshold: float = 90.0,
) -> bool:
    first_normalized = normalize_name(first)
    second_normalized = normalize_name(second)

    if first_normalized == second_normalized:
        return True

    similarity = ratio(
        first_normalized,
        second_normalized,
    )

    return similarity >= threshold


def deduplicate_entities(
    entities: list[Entity],
) -> list[Entity]:
    unique_entities: list[Entity] = []

    seen_urls: set[str] = set()

    for entity in entities:
        normalized_url = entity.url.strip().lower()

        # Exact URL duplicate
        if normalized_url and normalized_url in seen_urls:
            continue

        duplicate_found = False

        for existing in unique_entities:

            # Don't merge different entity types
            if entity.entity_type != existing.entity_type:
                continue

            if names_are_similar(
                entity.name,
                existing.name,
            ):
                duplicate_found = True
                break

        if duplicate_found:
            continue

        unique_entities.append(entity)

        if normalized_url:
            seen_urls.add(normalized_url)

    return unique_entities