from src.classification.entity import classify_entity
from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def article_to_entity(article: dict) -> Entity:
    article_url = normalize_url(article.get("url"))

    name = clean_text(article.get("title"))
    description = clean_text(article.get("description"))

    entity_type = classify_entity(
        name=name,
        description=description,
        source_type="News",
    )

    return Entity(
        id=f"news-{abs(hash(article_url))}",
        entity_type=entity_type,
        name=name,
        description=description,
        url=article_url,
        categories=["AI", "News"],
        source=Source(
            name=article.get("source_name", "Unknown"),
            url=article_url,
        ),
        metadata={
            "published": article.get("published"),
            "source_name": article.get("source_name"),
        },
    )


def articles_to_entities(
    articles: list[dict],
) -> list[Entity]:
    return [
        article_to_entity(article)
        for article in articles
    ]