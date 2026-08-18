import feedparser


AI_NEWS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
}


def fetch_news(
    limit_per_source: int = 10,
) -> list[dict]:
    articles = []

    for source_name, feed_url in AI_NEWS_FEEDS.items():
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit_per_source]:
            articles.append(
                {
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source_name": source_name,
                }
            )

    return articles