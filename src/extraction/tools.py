from src.classification.entity import classify_entity
from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def tool_to_entity(tool: dict) -> Entity:
    tool_id = tool.get("id", "")

    tool_url = normalize_url(
        f"https://huggingface.co/spaces/{tool_id}"
    )

    name = clean_text(tool_id)

    description = "AI application hosted on Hugging Face Spaces"

    entity_type = classify_entity(
        name=name,
        description=description,
        source_type="Hugging Face Space",
    )

    return Entity(
        id=f"tool-{tool_id}",
        entity_type="tool",
        name=name,
        description=description,
        url=tool_url,
        categories=["AI", "Tool", "Hugging Face Space"],
        source=Source(
            name="Hugging Face",
            url=tool_url,
        ),
        metadata={
            "likes": tool.get("likes", 0),
            "sdk": tool.get("sdk"),
            "tags": tool.get("tags", []),
            "created_at": tool.get("createdAt"),
            "private": tool.get("private", False),
        },
    )


def tools_to_entities(
    tools: list[dict],
) -> list[Entity]:
    return [
        tool_to_entity(tool)
        for tool in tools
    ]