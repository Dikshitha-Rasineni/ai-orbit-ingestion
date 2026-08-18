import re


ENTITY_TYPES = {
    "tool",
    "task",
    "company",
    "news",
    "video",
    "robot",
    "device",
    "model",
    "repository",
    "mcp",
    "collection",
    "personal",
    "creative",
    "recent",
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_entity(
    name: str,
    description: str = "",
    source_type: str = "",
) -> str:
    """
    Classify an entity using source information and
    keyword-based signals.
    """

    name_text = normalize_text(name)
    description_text = normalize_text(description)
    source_text = normalize_text(source_type)

    combined_text = (
        f"{name_text} "
        f"{description_text} "
        f"{source_text}"
    )

    # Strong source-based signals
    if source_text == "github":
        return "repository"

    if source_text == "youtube":
        return "video"

    if source_text in {"news", "rss"}:
        return "news"

    # MCP
    if "mcp server" in combined_text or "model context protocol" in combined_text:
        return "mcp"

    # Models
    model_keywords = [
        "language model",
        "foundation model",
        "machine learning model",
        "ai model",
        "llm",
        "diffusion model",
        "multimodal model",
    ]

    if any(keyword in combined_text for keyword in model_keywords):
        return "model"

    # Robotics
    robot_keywords = [
        "humanoid robot",
        "robotics system",
        "robot",
    ]

    if any(keyword in combined_text for keyword in robot_keywords):
        return "robot"

    # Hardware / devices
    device_keywords = [
        "ai hardware",
        "ai device",
        "gpu",
        "ai chip",
        "accelerator",
        "smart glasses",
        "robotic device",
    ]

    if any(keyword in combined_text for keyword in device_keywords):
        return "device"

    # Companies
    company_keywords = [
        "company",
        "startup",
        "founded",
        "headquartered",
        "inc.",
        "inc",
        "corp.",
        "corporation",
    ]

    if any(keyword in combined_text for keyword in company_keywords):
        return "company"

    # Creative tools
    creative_keywords = [
        "image generation",
        "video generation",
        "music generation",
        "generative art",
        "creative ai",
    ]

    if any(keyword in combined_text for keyword in creative_keywords):
        return "creative"

    # Personal assistants
    personal_keywords = [
        "personal assistant",
        "ai assistant",
        "virtual assistant",
    ]

    if any(keyword in combined_text for keyword in personal_keywords):
        return "personal"

    # Collections
    collection_keywords = [
        "curated list",
        "collection of",
        "directory of",
        "awesome list",
    ]

    if any(keyword in combined_text for keyword in collection_keywords):
        return "collection"

    # Default
    return "tool"