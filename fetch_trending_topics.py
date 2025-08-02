import feedparser

def get_trending_topics():
    feed_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"
    feed = feedparser.parse(feed_url)
    topics = []
    for entry in feed.entries:
        topics.append({"title": entry.title, "url": entry.link})
    return topics