from src.classification.entity import classify_entity
from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def model_to_entity(model: dict) -> Entity:
    model_id = model.get("id", "")

    model_url = normalize_url(
        f"https://huggingface.co/{model_id}"
    )

    name = clean_text(model_id)

    description = clean_text(
        model.get("pipeline_tag") or "AI/ML model hosted on Hugging Face"
    )

    entity_type = classify_entity(
        name=name,
        description=description,
        source_type="Hugging Face",
    )

    return Entity(
        id=f"huggingface-{model_id}",
        entity_type="model",
        name=name,
        description=description,
        url=model_url,
        categories=["AI", "Machine Learning", "Model"],
        source=Source(
            name="Hugging Face",
            url=model_url,
        ),
        metadata={
            "downloads": model.get("downloads", 0),
            "likes": model.get("likes", 0),
            "pipeline_tag": model.get("pipeline_tag"),
            "library_name": model.get("library_name"),
            "last_modified": model.get("lastModified"),
            "model_id": model_id,
        },
    )


def models_to_entities(
    models: list[dict],
) -> list[Entity]:
    return [
        model_to_entity(model)
        for model in models
    ]