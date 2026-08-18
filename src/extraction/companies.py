from src.cleaning.text import clean_text
from src.models import Entity, Source
from src.normalization.url import normalize_url


def company_to_entity(company: dict) -> Entity:
    company_url = normalize_url(company.get("url"))

    name = clean_text(company.get("name"))
    description = clean_text(company.get("description"))

    return Entity(
        id=f"company-{name.lower().replace(' ', '-')}",
        entity_type="company",
        name=name,
        description=description,
        url=company_url,
        categories=["AI", "Company"],
        source=Source(
            name="Company Website",
            url=company_url,
        ),
        metadata={
            "website_status": company.get("status_code"),
        },
    )


def companies_to_entities(
    companies: list[dict],
) -> list[Entity]:
    return [
        company_to_entity(company)
        for company in companies
    ]