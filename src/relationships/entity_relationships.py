from src.models import Entity


RELATIONSHIP_TYPES = {
    "owned_by",
    "supports_task",
    "uses_library",
    "uses_sdk",
    "published_by",
    "related_to",
}


def create_relationship(
    source: Entity,
    relationship: str,
    target: Entity,
) -> dict:
    if relationship not in RELATIONSHIP_TYPES:
        raise ValueError(
            f"Invalid relationship type: {relationship}"
        )

    return {
        "source_id": source.id,
        "relationship": relationship,
        "target_id": target.id,
    }


def build_relationships(
    entities: list[Entity],
) -> tuple[list[Entity], list[dict]]:

    relationships = []
    generated_entities = []

    companies = [
        e for e in entities
        if e.entity_type == "company"
    ]

    repositories = [
        e for e in entities
        if e.entity_type == "repository"
    ]

    models = [
        e for e in entities
        if e.entity_type == "model"
    ]

    tools = [
        e for e in entities
        if e.entity_type == "tool"
    ]

    news = [
        e for e in entities
        if e.entity_type == "news"
    ]

    videos = [
        e for e in entities
        if e.entity_type == "video"
    ]

    mcp_servers = [
        e for e in entities
        if e.entity_type == "mcp_server"
    ]

    # --------------------------------------------------
    # Company ownership aliases
    # --------------------------------------------------

    company_aliases = {
        "company-openai": {
            "openai",
        },
        "company-anthropic": {
            "anthropic",
        },
        "company-google-deepmind": {
            "google",
            "google-deepmind",
            "deepmind",
        },
        "company-nvidia": {
            "nvidia",
        },
        "company-meta-ai": {
            "meta",
            "facebook",
        },
        "company-microsoft-ai": {
            "microsoft",
        },
        "company-hugging-face": {
            "huggingface",
            "hugging-face",
        },
        "company-mistral-ai": {
            "mistral",
        },
        "company-cohere": {
            "cohere",
        },
        "company-xai": {
            "xai",
        },
        "company-ai21-labs": {
            "ai21",
        },
        "company-scale-ai": {
            "scale",
        },
    }

    # --------------------------------------------------
    # Repository / Tool / MCP → owned_by → Company
    # --------------------------------------------------

    owned_entities = (
        repositories
        + tools
        + mcp_servers
    )

    for entity in owned_entities:

        owner = str(
            entity.metadata.get(
                "owner",
                "",
            )
        ).lower().strip()

        if not owner:
            continue

        for company in companies:

            aliases = company_aliases.get(
                company.id,
                set(),
            )

            if owner in aliases:

                relationships.append(
                    create_relationship(
                        entity,
                        "owned_by",
                        company,
                    )
                )

    # --------------------------------------------------
    # Model → supports_task → Task
    # --------------------------------------------------

    task_entities = {}

    for model in models:

        pipeline_tag = model.metadata.get(
            "pipeline_tag"
        )

        if not pipeline_tag:
            continue

        task_id = f"task-{pipeline_tag}"

        if task_id not in task_entities:

            task_entity = Entity(
                id=task_id,
                entity_type="task",
                name=pipeline_tag,
                description=(
                    f"Model pipeline task: "
                    f"{pipeline_tag}"
                ),
                url="",
                categories=[
                    "AI",
                    "Task",
                ],
                source=model.source,
                metadata={},
            )

            task_entities[task_id] = (
                task_entity
            )

            generated_entities.append(
                task_entity
            )

        relationships.append(
            create_relationship(
                model,
                "supports_task",
                task_entities[task_id],
            )
        )

    # --------------------------------------------------
    # Model → uses_library → Library
    # --------------------------------------------------

    library_entities = {}

    for model in models:

        library = model.metadata.get(
            "library_name"
        )

        if not library:
            continue

        library_id = (
            f"library-{library.lower()}"
        )

        if library_id not in library_entities:

            library_entity = Entity(
                id=library_id,
                entity_type="library",
                name=library,
                description=(
                    f"Machine learning library "
                    f"associated with {model.name}"
                ),
                url="",
                categories=[
                    "AI",
                    "Library",
                ],
                source=model.source,
                metadata={},
            )

            library_entities[library_id] = (
                library_entity
            )

            generated_entities.append(
                library_entity
            )

        relationships.append(
            create_relationship(
                model,
                "uses_library",
                library_entities[library_id],
            )
        )

    # --------------------------------------------------
    # Tool / MCP → uses_sdk → SDK
    # --------------------------------------------------

    sdk_entities = {}

    for entity in tools + mcp_servers:

        sdk = entity.metadata.get("sdk")

        if not sdk:
            continue

        sdk_id = f"sdk-{sdk.lower()}"

        if sdk_id not in sdk_entities:

            sdk_entity = Entity(
                id=sdk_id,
                entity_type="sdk",
                name=sdk,
                description=(
                    f"SDK/runtime associated "
                    f"with {entity.name}"
                ),
                url="",
                categories=[
                    "AI",
                    "SDK",
                ],
                source=entity.source,
                metadata={},
            )

            sdk_entities[sdk_id] = (
                sdk_entity
            )

            generated_entities.append(
                sdk_entity
            )

        relationships.append(
            create_relationship(
                entity,
                "uses_sdk",
                sdk_entities[sdk_id],
            )
        )

    # --------------------------------------------------
    # News / Video → published_by → Source
    # --------------------------------------------------

    source_entities = {}

    for entity in news + videos:

        source_name = entity.metadata.get(
            "source_name"
        )

        if not source_name:
            continue

        source_id = (
            "source-"
            + source_name.lower()
            .replace(" ", "-")
        )

        if source_id not in source_entities:

            source_entity = Entity(
                id=source_id,
                entity_type="source",
                name=source_name,
                description=(
                    f"Content source: "
                    f"{source_name}"
                ),
                url=entity.source.url,
                categories=[
                    "Source"
                ],
                source=entity.source,
                metadata={},
            )

            source_entities[source_id] = (
                source_entity
            )

            generated_entities.append(
                source_entity
            )

        relationships.append(
            create_relationship(
                entity,
                "published_by",
                source_entities[source_id],
            )
        )

    # --------------------------------------------------
    # Remove duplicate relationships
    # --------------------------------------------------

    unique = {}

    for relationship in relationships:

        key = (
            relationship["source_id"],
            relationship["relationship"],
            relationship["target_id"],
        )

        unique[key] = relationship

    return (
        generated_entities,
        list(unique.values()),
    )