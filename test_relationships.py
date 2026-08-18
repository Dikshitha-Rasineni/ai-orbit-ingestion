import json

from src.models import Entity, Source
from src.relationships.entity_relationships import (
    build_relationships,
)
from src.validation.export import (
    export_graph_entities,
    export_relationships,
)


def load_entities():

    with open(
        "data/entities.json",
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return [
        Entity(
            id=item["id"],
            entity_type=item["entity_type"],
            name=item["name"],
            description=item.get(
                "description",
                "",
            ),
            url=item.get(
                "url",
                "",
            ),
            categories=item.get(
                "categories",
                [],
            ),
            source=Source(
                name=item["source"]["name"],
                url=item["source"]["url"],
            ),
            metadata=item.get(
                "metadata",
                {},
            ),
        )
        for item in data
    ]


def main():

    entities = load_entities()

    generated_entities, relationships = (
        build_relationships(entities)
    )

    all_entities = (
        entities + generated_entities
    )

    print(
        f"Original entities: {len(entities)}"
    )

    print(
        f"Generated graph entities: "
        f"{len(generated_entities)}"
    )

    print(
        f"Total graph entities: "
        f"{len(all_entities)}"
    )

    print(
        f"Relationships: "
        f"{len(relationships)}"
    )

    # Show a few relationships
    print("\nSample relationships:")

    for relationship in relationships[:10]:
        print(relationship)

    # Export graph entities
    export_graph_entities(
        all_entities
    )

    # Export relationships
    export_relationships(
        relationships
    )


if __name__ == "__main__":
    main()