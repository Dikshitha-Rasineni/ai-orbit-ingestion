import json
from pathlib import Path


GRAPH_PATH = Path("data/graph_entities.json")
RELATIONSHIPS_PATH = Path("data/relationships.json")


def load_graph():
    with open(
        GRAPH_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        entities = json.load(file)

    with open(
        RELATIONSHIPS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        relationships = json.load(file)

    return entities, relationships


def find_entity(entity_id: str):
    entities, _ = load_graph()

    for entity in entities:
        if entity["id"] == entity_id:
            return entity

    return None


def find_by_name(name: str):
    entities, _ = load_graph()

    query = name.lower().strip()

    return [
        entity
        for entity in entities
        if query in entity.get(
            "name",
            "",
        ).lower()
    ]


def find_by_type(entity_type: str):
    entities, _ = load_graph()

    return [
        entity
        for entity in entities
        if entity.get("entity_type")
        == entity_type
    ]


def find_relationships(entity_id: str):
    _, relationships = load_graph()

    return [
        relationship
        for relationship in relationships
        if (
            relationship["source_id"]
            == entity_id
            or relationship["target_id"]
            == entity_id
        )
    ]


def get_neighbors(entity_id: str):
    entities, relationships = load_graph()

    entity_map = {
        entity["id"]: entity
        for entity in entities
    }

    neighbors = []

    for relationship in relationships:

        if relationship["source_id"] == entity_id:

            target_id = relationship["target_id"]

            if target_id in entity_map:
                neighbors.append(
                    entity_map[target_id]
                )

        elif relationship["target_id"] == entity_id:

            source_id = relationship["source_id"]

            if source_id in entity_map:
                neighbors.append(
                    entity_map[source_id]
                )

    return neighbors


def find_by_relationship(
    relationship: str | None = None,
    source_id: str | None = None,
    target_id: str | None = None,
):
    """
    Find relationships using any combination of:

        relationship
        source_id
        target_id

    Example:

        find_by_relationship(
            "owned_by"
        )

    or:

        find_by_relationship(
            relationship="owned_by"
        )
    """

    _, relationships = load_graph()

    results = relationships

    if relationship is not None:
        results = [
            item
            for item in results
            if item.get("relationship")
            == relationship
        ]

    if source_id is not None:
        results = [
            item
            for item in results
            if item.get("source_id")
            == source_id
        ]

    if target_id is not None:
        results = [
            item
            for item in results
            if item.get("target_id")
            == target_id
        ]

    return results


def _metadata_contains(
    metadata,
    query: str,
) -> bool:
    """
    Recursively search metadata keys
    and values.
    """

    if not metadata:
        return False

    if isinstance(metadata, dict):

        for key, value in metadata.items():

            if query in str(key).lower():
                return True

            if _metadata_contains(
                value,
                query,
            ):
                return True

        return False

    if isinstance(metadata, list):

        return any(
            _metadata_contains(
                value,
                query,
            )
            for value in metadata
        )

    return query in str(
        metadata
    ).lower()


def search(query: str):
    """
    Search the complete graph.

    Searches:

    - name
    - entity type
    - description
    - URL
    - categories
    - source
    - metadata keys
    - metadata values
    """

    entities, _ = load_graph()

    query = query.lower().strip()

    if not query:
        return []

    results = []

    for entity in entities:

        name = str(
            entity.get(
                "name",
                "",
            )
        ).lower()

        entity_type = str(
            entity.get(
                "entity_type",
                "",
            )
        ).lower()

        description = str(
            entity.get(
                "description",
                "",
            )
        ).lower()

        url = str(
            entity.get(
                "url",
                "",
            )
        ).lower()

        categories = " ".join(
            str(category).lower()
            for category in entity.get(
                "categories",
                [],
            )
        )

        source = entity.get(
            "source",
            {},
        )

        source_text = " ".join(
            [
                str(
                    source.get(
                        "name",
                        "",
                    )
                ).lower(),
                str(
                    source.get(
                        "url",
                        "",
                    )
                ).lower(),
            ]
        )

        basic_match = (
            query in name
            or query in entity_type
            or query in description
            or query in url
            or query in categories
            or query in source_text
        )

        metadata_match = _metadata_contains(
            entity.get(
                "metadata",
                {},
            ),
            query,
        )

        if basic_match or metadata_match:
            results.append(entity)

    return results