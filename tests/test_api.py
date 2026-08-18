from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_openai_entity():
    response = client.get(
        "/entities/company-openai"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "company-openai"
    assert data["entity_type"] == "company"
    assert data["name"] == "OpenAI"


def test_companies():
    response = client.get(
        "/entities",
        params={
            "entity_type": "company"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= 30


def test_search_openai():
    response = client.get(
        "/search",
        params={
            "q": "OpenAI"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] > 0


def test_search_docker():
    response = client.get(
        "/search",
        params={
            "q": "docker"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] > 0


def test_microsoft_relationships():
    response = client.get(
        "/entities/company-microsoft-ai/relationships"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 4


def test_microsoft_neighbors():
    response = client.get(
        "/entities/company-microsoft-ai/neighbors"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 4


def test_owned_by_relationships():
    response = client.get(
        "/relationships",
        params={
            "relationship": "owned_by"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= 4


def test_missing_entity():
    response = client.get(
        "/entities/does-not-exist"
    )

    assert response.status_code == 404


def test_diffusers_search():
    response = client.get(
        "/search",
        params={
            "q": "diffusers"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] > 0