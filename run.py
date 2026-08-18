from src.discovery.github import (
    search_github_repositories,
)

from src.discovery.huggingface import (
    search_huggingface_models,
)

from src.discovery.news import (
    fetch_news,
)

from src.discovery.youtube import (
    fetch_youtube_videos,
)

from src.discovery.tools import (
    search_ai_tools,
)

from src.discovery.companies import (
    fetch_companies,
)

from src.discovery.mcp import (
    search_mcp_servers,
)


from src.extraction.github import (
    repositories_to_entities,
)

from src.extraction.huggingface import (
    models_to_entities,
)

from src.extraction.news import (
    articles_to_entities,
)

from src.extraction.youtube import (
    videos_to_entities,
)

from src.extraction.tools import (
    tools_to_entities,
)

from src.extraction.companies import (
    companies_to_entities,
)

from src.extraction.mcp import (
    mcp_servers_to_entities,
)


from src.deduplication.entity import (
    deduplicate_entities,
)

from src.validation.export import (
    export_entities,
    export_graph_entities,
    export_relationships,
)

from src.relationships.entity_relationships import (
    build_relationships,
)


def main():

    # ==================================================
    # DISCOVERY
    # ==================================================

    github_repositories = search_github_repositories(
        "artificial intelligence",
        55,
    )

    huggingface_models = search_huggingface_models(
        limit=50,
    )

    news_articles = fetch_news(
        limit_per_source=30,
    )

    youtube_videos = fetch_youtube_videos(
        limit_per_source=30,
    )

    ai_tools = search_ai_tools(
        limit=40,
    )

    ai_companies = fetch_companies(
        limit=30,
    )

    mcp_servers = search_mcp_servers(
        limit=26,
    )

    # ==================================================
    # EXTRACTION
    # ==================================================

    github_entities = repositories_to_entities(
        github_repositories
    )

    huggingface_entities = models_to_entities(
        huggingface_models
    )

    news_entities = articles_to_entities(
        news_articles
    )

    youtube_entities = videos_to_entities(
        youtube_videos
    )

    tool_entities = tools_to_entities(
        ai_tools
    )

    company_entities = companies_to_entities(
        ai_companies
    )

    mcp_entities = mcp_servers_to_entities(
        mcp_servers
    )

    # ==================================================
    # COMBINE ALL ENTITIES
    # ==================================================

    entities = (
        github_entities
        + huggingface_entities
        + news_entities
        + youtube_entities
        + tool_entities
        + company_entities
        + mcp_entities
    )

    total_before_dedup = len(entities)

    # ==================================================
    # DEDUPLICATION
    # ==================================================

    entities = deduplicate_entities(
        entities
    )

    # ==================================================
    # EXPORT ORIGINAL ENTITIES
    # ==================================================

    export_entities(
        entities
    )

    # ==================================================
    # PIPELINE SUMMARY
    # ==================================================

    print()
    print("Pipeline Summary")
    print("-" * 30)

    print(
        f"GitHub:       {len(github_repositories)}"
    )

    print(
        f"Hugging Face: {len(huggingface_models)}"
    )

    print(
        f"News:         {len(news_articles)}"
    )

    print(
        f"YouTube:      {len(youtube_videos)}"
    )

    print(
        f"Tools:        {len(ai_tools)}"
    )

    print(
        f"Companies:    {len(ai_companies)}"
    )

    print(
        f"MCP Servers:  {len(mcp_servers)}"
    )

    print(
        f"Total:        {total_before_dedup}"
    )

    print(
        f"After Dedup:  {len(entities)}"
    )

    # ==================================================
    # BUILD RELATIONSHIP GRAPH
    # ==================================================

    print()
    print("Building relationship graph...")

    generated_entities, relationships = (
        build_relationships(
            entities
        )
    )

    graph_entities = (
        entities
        + generated_entities
    )

    print(
        f"Generated graph entities: "
        f"{len(generated_entities)}"
    )

    print(
        f"Graph entities: "
        f"{len(graph_entities)}"
    )

    print(
        f"Relationships: "
        f"{len(relationships)}"
    )

    # ==================================================
    # EXPORT GRAPH
    # ==================================================

    export_graph_entities(
        graph_entities
    )

    export_relationships(
        relationships
    )

    # ==================================================
    # GRAPH VALIDATION
    # ==================================================

    entity_ids = {
        entity.id
        for entity in graph_entities
    }

    missing_sources = [
        relationship
        for relationship in relationships
        if relationship["source_id"]
        not in entity_ids
    ]

    missing_targets = [
        relationship
        for relationship in relationships
        if relationship["target_id"]
        not in entity_ids
    ]

    # ==================================================
    # VALIDATION SUMMARY
    # ==================================================

    print()
    print("Graph Validation")
    print("-" * 30)

    print(
        f"Graph entities:  "
        f"{len(graph_entities)}"
    )

    print(
        f"Relationships:   "
        f"{len(relationships)}"
    )

    print(
        f"Missing sources: "
        f"{len(missing_sources)}"
    )

    print(
        f"Missing targets: "
        f"{len(missing_targets)}"
    )

    # ==================================================
    # VALIDATION RESULT
    # ==================================================

    if (
        not missing_sources
        and not missing_targets
    ):

        print()
        print(
            "✓ Graph validation passed"
        )

    else:

        print()
        print(
            "✗ Graph validation failed"
        )

        if missing_sources:
            print()
            print(
                "Example missing source:"
            )
            print(
                missing_sources[0]
            )

        if missing_targets:
            print()
            print(
                "Example missing target:"
            )
            print(
                missing_targets[0]
            )


if __name__ == "__main__":
    main()