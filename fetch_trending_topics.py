import feedparser

def get_trending_topics():
    #feed_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"
    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)
    topics = []
    for entry in feed.entries:
        topics.append({"title": entry.title, "url": entry.link})
    print(f"Fetched {len(topics)} trending topics.")
    return topics
