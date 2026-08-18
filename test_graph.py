from src.graph.query import (
    find_entity,
    find_by_name,
    find_by_type,
    find_relationships,
    get_neighbors,
    find_by_relationship,
    search,
)


def main():

    print("=" * 60)
    print("GRAPH QUERY TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Find entity by ID
    # --------------------------------------------------

    entity = find_entity("company-openai")

    print("\nOpenAI:")
    print(entity)

    # --------------------------------------------------
    # 2. Search by name
    # --------------------------------------------------

    results = find_by_name("OpenAI")

    print(
        f"\nEntities matching 'OpenAI': {len(results)}"
    )

    for result in results[:5]:
        print(
            result["id"],
            "→",
            result["name"],
        )

    # --------------------------------------------------
    # 3. Find entities by type
    # --------------------------------------------------

    companies = find_by_type("company")

    print(
        f"\nCompanies: {len(companies)}"
    )

    # --------------------------------------------------
    # 4. Find relationships for Microsoft
    # --------------------------------------------------

    microsoft_relationships = find_relationships(
        "company-microsoft-ai"
    )

    print(
        f"\nMicrosoft relationships: "
        f"{len(microsoft_relationships)}"
    )

    for relationship in microsoft_relationships:
        print(relationship)

    # --------------------------------------------------
    # 5. Get Microsoft neighbors
    # --------------------------------------------------

    neighbors = get_neighbors(
        "company-microsoft-ai"
    )

    print(
        f"\nMicrosoft neighbors: "
        f"{len(neighbors)}"
    )

    for neighbor in neighbors:
        print(
            neighbor["entity_type"],
            "→",
            neighbor["name"],
        )

    # --------------------------------------------------
    # 6. Find relationships by type
    # --------------------------------------------------

    owned_by = find_by_relationship(
        relationship="owned_by"
    )

    print(
        f"\nowned_by relationships: "
        f"{len(owned_by)}"
    )

    # --------------------------------------------------
    # 7. Metadata search
    #
    # The current dataset does NOT contain
    # text-to-image, so use "diffusers".
    # --------------------------------------------------

    search_results = search("diffusers")

    print(
        f"\nSearch results for 'diffusers': "
        f"{len(search_results)}"
    )

    for result in search_results[:5]:
        print(
            result["id"],
            "→",
            result["name"],
        )

    # --------------------------------------------------
    # 8. Search another common metadata value
    # --------------------------------------------------

    docker_results = search("docker")

    print(
        f"\nSearch results for 'docker': "
        f"{len(docker_results)}"
    )

    for result in docker_results[:5]:
        print(
            result["id"],
            "→",
            result["name"],
        )

    print("\n" + "=" * 60)
    print("GRAPH QUERY TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()