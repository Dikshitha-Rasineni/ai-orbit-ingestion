import feedparser


YOUTUBE_FEEDS = {
    "Google DeepMind": "https://www.youtube.com/feeds/videos.xml?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw",
    "OpenAI": "https://www.youtube.com/feeds/videos.xml?channel_id=UCXZCJLdBC09xxGZ6gcdrc6A",
}


def fetch_youtube_videos(
    limit_per_source: int = 10,
) -> list[dict]:
    videos = []

    for source_name, feed_url in YOUTUBE_FEEDS.items():
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit_per_source]:
            videos.append(
                {
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source_name": source_name,
                }
            )

    return videos