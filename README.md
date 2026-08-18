# AI Orbit Ingestion

AI Orbit Ingestion is an end-to-end AI knowledge graph pipeline that discovers, extracts, normalizes, deduplicates, and connects AI ecosystem entities from multiple sources.

The system converts information from different AI-related sources into a structured entity graph and exposes the graph through a query layer and FastAPI.

---

## Architecture

```text
Discovery
    ↓
Extraction
    ↓
Normalization
    ↓
Deduplication
    ↓
Entity Store
    ↓
Relationship Builder
    ↓
Knowledge Graph
    ↓
Query Layer
    ↓
FastAPI
```

---

## Data Sources

The pipeline currently collects information from:

- GitHub repositories
- Hugging Face models
- AI news
- YouTube videos
- AI tools
- AI companies
- MCP servers

---

## Current Dataset

The latest successful pipeline run produced:

| Metric | Count |
|---|---:|
| Source entities | 256 |
| Generated graph entities | 31 |
| Total graph entities | 287 |
| Relationships | 187 |
| Missing relationship sources | 0 |
| Missing relationship targets | 0 |

The ingestion pipeline originally discovered 261 records before deduplication.

```text
GitHub:        55
Hugging Face:  50
News:          30
YouTube:       30
Tools:         40
Companies:     30
MCP Servers:   26
-------------------
Total:        261
After Dedup:  256
```

---

## Entity Types

The graph contains the following entity types:

- `company`
- `repository`
- `model`
- `news`
- `video`
- `tool`
- `mcp_server`
- `task`
- `library`
- `sdk`
- `source`

---

## Relationship Types

The graph supports relationships including:

- `owned_by`
- `supports_task`
- `uses_library`
- `uses_sdk`
- `published_by`
- `related_to`

Relationships are stored using source and target entity IDs.

Example:

```json
{
  "source_id": "github-373462930",
  "relationship": "owned_by",
  "target_id": "company-microsoft-ai"
}
```

---

## Project Structure

```text
ai-orbit-ingestion/
│
├── data/
│   ├── entities.json
│   ├── graph_entities.json
│   └── relationships.json
│
├── src/
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── discovery/
│   │   ├── __init__.py
│   │   ├── companies.py
│   │   ├── github.py
│   │   ├── huggingface.py
│   │   ├── mcp.py
│   │   ├── news.py
│   │   ├── tools.py
│   │   └── youtube.py
│   │
│   ├── extraction/
│   │   ├── __init__.py
│   │   ├── companies.py
│   │   ├── github.py
│   │   ├── huggingface.py
│   │   ├── mcp.py
│   │   ├── news.py
│   │   ├── tools.py
│   │   └── youtube.py
│   │
│   ├── graph/
│   │   └── query.py
│   │
│   ├── relationships/
│   │   └── entity_relationships.py
│   │
│   ├── validation/
│   │   └── export.py
│   │
│   └── models.py
│
├── tests/
│   └── test_api.py
│
├── run.py
├── test_graph.py
├── test_relationships.py
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ai-orbit-ingestion
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
```

## 3. Activate the environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Install dependencies

Install the project's required packages.

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the main runtime dependencies:

```bash
pip install fastapi uvicorn pytest httpx2 requests feedparser pydantic
```

---

# Running the Ingestion Pipeline

Run:

```bash
python run.py
```

The pipeline performs:

1. Discovery
2. Extraction
3. Entity normalization
4. Deduplication
5. Relationship construction
6. Graph generation
7. Graph validation
8. JSON export

A successful run produces:

```text
Saved 256 entities → data/entities.json

Pipeline Summary
------------------------------
GitHub:        55
Hugging Face:  50
News:          30
YouTube:       30
Tools:         40
Companies:     30
MCP Servers:   26
Total:        261
After Dedup:  256

Building relationship graph...

Generated graph entities: 31
Graph entities: 287
Relationships: 187

Saved 287 graph entities → data/graph_entities.json
Saved 187 relationships → data/relationships.json

Graph Validation
------------------------------
Graph entities: 287
Relationships:  187
Missing sources: 0
Missing targets: 0

✓ Graph validation passed
```

---

# Generated Data

The pipeline generates three primary JSON files.

## `data/entities.json`

Contains the normalized and deduplicated source entities.

Example:

```json
{
  "id": "company-openai",
  "entity_type": "company",
  "name": "OpenAI",
  "description": "AI research and deployment company developing artificial intelligence systems and products."
}
```

## `data/graph_entities.json`

Contains all source entities plus generated graph entities such as:

- tasks
- libraries
- SDKs
- sources

Current total:

```text
287 graph entities
```

## `data/relationships.json`

Contains graph relationships connecting entities.

Current total:

```text
187 relationships
```

---

# Graph Validation

Every relationship is validated against the graph entity set.

The validation checks that:

- Every relationship source exists.
- Every relationship target exists.
- Relationship records contain valid IDs.
- Duplicate relationships are removed.

Successful validation:

```text
Missing sources: 0
Missing targets: 0

✓ Graph validation passed
```

---

# Graph Query Layer

The project contains a query layer in:

```text
src/graph/query.py
```

It provides functions for:

- Loading the graph
- Finding an entity by ID
- Finding entities by name
- Filtering entities by type
- Finding relationships
- Finding neighbors
- Filtering relationships
- Searching graph entities

The available functions are:

```python
load_graph()
find_entity()
find_by_name()
find_by_type()
find_relationships()
get_neighbors()
find_by_relationship()
search()
```

---

# FastAPI

The graph is exposed through a FastAPI application.

Start the server:

```bash
uvicorn src.api.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Root

```http
GET /
```

Returns API information and status.

---

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## Get Entity

```http
GET /entities/{entity_id}
```

Example:

```text
/entities/company-openai
```

Returns the requested entity.

---

## Filter Entities by Type

```http
GET /entities?entity_type=company
```

Example:

```text
/entities?entity_type=company
```

Returns all entities belonging to the requested type.

---

## Search Entities

```http
GET /search?q={query}
```

Example:

```text
/search?q=OpenAI
```

Another example:

```text
/search?q=docker
```

---

## Search by Name

```http
GET /entities/search/name?q={query}
```

Example:

```text
/entities/search/name?q=OpenAI
```

---

## Get Entity Relationships

```http
GET /entities/{entity_id}/relationships
```

Example:

```text
/entities/company-microsoft-ai/relationships
```

---

## Get Entity Neighbors

```http
GET /entities/{entity_id}/neighbors
```

Example:

```text
/entities/company-microsoft-ai/neighbors
```

This returns entities connected to the specified entity through graph relationships.

---

## Filter Relationships

```http
GET /relationships
```

Optional filters:

```text
/relationships?relationship=owned_by
```

```text
/relationships?source_id=company-microsoft-ai
```

```text
/relationships?target_id=company-microsoft-ai
```

---

# Example Graph Queries

## Find OpenAI

```text
GET /entities/company-openai
```

---

## Search for OpenAI

```text
GET /search?q=OpenAI
```

---

## Search for Docker

```text
GET /search?q=docker
```

---

## Find Microsoft AI neighbors

```text
GET /entities/company-microsoft-ai/neighbors
```

---

## Find Microsoft AI relationships

```text
GET /entities/company-microsoft-ai/relationships
```

---

## Find all companies

```text
GET /entities?entity_type=company
```

---

## Find ownership relationships

```text
GET /relationships?relationship=owned_by
```

---

# Testing

The project includes automated API tests using `pytest`.

Run:

```bash
pytest -v
```

The current test suite contains 11 tests.

Latest verified result:

```text
11 passed in 0.29s
```

Tests cover:

- Root endpoint
- Health endpoint
- Entity lookup
- Company filtering
- OpenAI search
- Docker search
- Microsoft relationships
- Microsoft neighbors
- `owned_by` relationships
- Missing entity handling
- Diffusers metadata search

---

# Verification

The complete system has been verified end-to-end.

```text
Discovery                 PASS
Extraction                PASS
Normalization             PASS
Deduplication             PASS
Entity storage            PASS
Relationship generation   PASS
Graph construction        PASS
Graph validation          PASS
Graph queries             PASS
FastAPI                   PASS
Swagger documentation     PASS
Automated tests            PASS
```

Final verified graph:

```text
Graph entities: 287
Relationships:  187

Missing sources: 0
Missing targets: 0
```

Final automated test result:

```text
11 passed
```

---

# End-to-End Flow

```text
GitHub
Hugging Face
News
YouTube
AI Tools
Companies
MCP Servers
       │
       ▼
   Discovery
       │
       ▼
   Extraction
       │
       ▼
 Normalization
       │
       ▼
 Deduplication
       │
       ▼
 Entity Store
       │
       ▼
Relationship Builder
       │
       ▼
 Knowledge Graph
       │
       ├── Entity Search
       ├── Relationship Search
       ├── Neighbor Traversal
       └── Metadata Search
       │
       ▼
    FastAPI
       │
       ▼
 Swagger UI / API Clients
```

---

# Project Status

The current implementation provides a complete working pipeline from multi-source AI data ingestion to a validated knowledge graph and queryable REST API.

```text
✓ Multi-source ingestion
✓ Entity extraction
✓ Deduplication
✓ Relationship generation
✓ Graph construction
✓ Graph validation
✓ Query layer
✓ REST API
✓ Swagger documentation
✓ Automated testing
✓ Project documentation
```

---

## License

Add the project's applicable license here.