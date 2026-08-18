from fastapi import FastAPI, HTTPException, Query

from src.graph.query import (
    find_entity,
    find_by_name,
    find_by_type,
    find_relationships,
    get_neighbors,
    find_by_relationship,
    search,
)


app = FastAPI(
    title="AI Orbit Knowledge Graph API",
    description=(
        "Query API for the AI Orbit entity "
        "and relationship graph."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "name": "AI Orbit Knowledge Graph API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/entities/{entity_id}")
def get_entity(entity_id: str):

    entity = find_entity(entity_id)

    if entity is None:
        raise HTTPException(
            status_code=404,
            detail="Entity not found",
        )

    return entity


@app.get("/entities")
def entities_by_type(
    entity_type: str = Query(
        ...,
        description="Entity type, e.g. company, repository, model",
    )
):

    results = find_by_type(entity_type)

    return {
        "count": len(results),
        "entities": results,
    }


@app.get("/search")
def search_entities(
    q: str = Query(
        ...,
        min_length=1,
        description="Search query",
    )
):

    results = search(q)

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.get("/entities/search/name")
def search_by_name(
    q: str = Query(
        ...,
        min_length=1,
    )
):

    results = find_by_name(q)

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.get("/entities/{entity_id}/relationships")
def entity_relationships(
    entity_id: str,
):

    entity = find_entity(entity_id)

    if entity is None:
        raise HTTPException(
            status_code=404,
            detail="Entity not found",
        )

    relationships = find_relationships(
        entity_id
    )

    return {
        "entity_id": entity_id,
        "count": len(relationships),
        "relationships": relationships,
    }


@app.get("/entities/{entity_id}/neighbors")
def entity_neighbors(
    entity_id: str,
):

    entity = find_entity(entity_id)

    if entity is None:
        raise HTTPException(
            status_code=404,
            detail="Entity not found",
        )

    neighbors = get_neighbors(
        entity_id
    )

    return {
        "entity_id": entity_id,
        "count": len(neighbors),
        "neighbors": neighbors,
    }


@app.get("/relationships")
def relationships(
    relationship: str | None = None,
    source_id: str | None = None,
    target_id: str | None = None,
):

    results = find_by_relationship(
        relationship=relationship,
        source_id=source_id,
        target_id=target_id,
    )

    return {
        "count": len(results),
        "relationships": results,
    }