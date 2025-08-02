# ---------------------------- fetch_trending_topics.py ----------------------------
import feedparser

def get_trending_topics():
    feed_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"
    feed = feedparser.parse(feed_url)
    topics = []
    for entry in feed.entries:
        topics.append({"title": entry.title, "url": entry.link})
    return topics


# ---------------------------- generate_content.py ----------------------------
# This is a placeholder; replace with real API like OpenAI or Gemini

def generate_blog_content(title):
    return f"<h2>{title}</h2>\n<p>This is AI-generated content for the topic: {title}</p>"


# ---------------------------- tagging_and_category.py ----------------------------
def detect_category_and_tags(content):
    # Simple keyword detection for demonstration
    tags = []
    if "finance" in content.lower():
        category = "Finance"
        tags = ["money", "finance", "investment"]
    elif "technology" in content.lower():
        category = "Technology"
        tags = ["tech", "AI", "gadgets"]
    else:
        category = "General"
        tags = ["trending", "news"]
    return category, tags


# ---------------------------- post_to_blogger.py ----------------------------
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

SCOPES = ["https://www.googleapis.com/auth/blogger"]


def get_blogger_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("blogger", "v3", credentials=creds)
    return service


def post_blog(title, content, category, tags):
    service = get_blogger_service()
    blog_id = "your-blog-id-here"  # Replace with your actual blog ID
    post = {
        "kind": "blogger#post",
        "title": title,
        "labels": tags,
        "content": content,
    }
    try:
        service.posts().insert(blogId=blog_id, body=post).execute()
        return True
    except Exception as e:
        print("Failed to post:", e)
        return False


# ---------------------------- tracker.py ----------------------------
import json
import os

POSTED_FILE = "posted_topics.json"

def load_posted():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_posted_topic(title):
    posted = load_posted()
    posted.add(title)
    with open(POSTED_FILE, "w") as f:
        json.dump(list(posted), f)

def is_duplicate(title):
    return title in load_posted()


# ---------------------------- main.py ----------------------------
from fetch_trending_topics import get_trending_topics
from generate_content import generate_blog_content
from tagging_and_category import detect_category_and_tags
from post_to_blogger import post_blog
from tracker import is_duplicate, save_posted_topic


def main():
    topics = get_trending_topics()
    for topic in topics:
        title = topic["title"]
        if is_duplicate(title):
            print(f"Skipping duplicate: {title}")
            continue
        content = generate_blog_content(title)
        category, tags = detect_category_and_tags(content)
        success = post_blog(title, content, category, tags)
        if success:
            print(f"Posted: {title}")
            save_posted_topic(title)
        else:
            print(f"Failed to post: {title}")


if __name__ == "__main__":
    main()
