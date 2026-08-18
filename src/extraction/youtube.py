from src.classification.entity import classify_entity
from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def video_to_entity(video: dict) -> Entity:
    video_url = normalize_url(video.get("url"))

    name = clean_text(video.get("title"))
    description = clean_text(video.get("description"))

    entity_type = classify_entity(
        name=name,
        description=description,
        source_type="YouTube",
    )

    return Entity(
        id=f"youtube-{abs(hash(video_url))}",
        entity_type=entity_type,
        name=name,
        description=description,
        url=video_url,
        categories=["AI", "Video"],
        source=Source(
            name=video.get("source_name", "YouTube"),
            url=video_url,
        ),
        metadata={
            "published": video.get("published"),
            "source_name": video.get("source_name"),
        },
    )


def videos_to_entities(
    videos: list[dict],
) -> list[Entity]:
    return [
        video_to_entity(video)
        for video in videos
    ]