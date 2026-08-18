import json
from pathlib import Path

from src.models import Entity


ENTITIES_OUTPUT_PATH = Path(
    "data/entities.json"
)

GRAPH_ENTITIES_OUTPUT_PATH = Path(
    "data/graph_entities.json"
)

RELATIONSHIPS_OUTPUT_PATH = Path(
    "data/relationships.json"
)


def export_entities(
    entities: list[Entity],
) -> None:

    ENTITIES_OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    data = [
        entity.model_dump()
        for entity in entities
    ]

    with open(
        ENTITIES_OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved {len(data)} entities → "
        f"{ENTITIES_OUTPUT_PATH}"
    )


def export_graph_entities(
    entities: list[Entity],
) -> None:

    GRAPH_ENTITIES_OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    data = [
        entity.model_dump()
        for entity in entities
    ]

    with open(
        GRAPH_ENTITIES_OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved {len(data)} graph entities → "
        f"{GRAPH_ENTITIES_OUTPUT_PATH}"
    )


def export_relationships(
    relationships: list[dict],
) -> None:

    RELATIONSHIPS_OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with open(
        RELATIONSHIPS_OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            relationships,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved {len(relationships)} relationships → "
        f"{RELATIONSHIPS_OUTPUT_PATH}"
    )