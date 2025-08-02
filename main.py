import os
import logging
from fetch_trending_topics import get_trending_topics
from generate_content import generate_blog_content
from tagging_and_category import detect_category_and_tags
from post_to_blogger import post_blog
from tracker import is_duplicate, save_posted_topic

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    topics = get_trending_topics()
    if not topics:
        logging.info("No trending topics found.")
        return

    for topic in topics:
        title = topic["title"]
        print(f"Processing topic: {title}")
        # Check if the topic has already been posted
        if is_duplicate(title):
            print(f"Skipping duplicate: {title}")
            continue
        content = generate_blog_content(title, GEMINI_API_KEY)
        category, tags = detect_category_and_tags(content)
        success = post_blog(title, content, category, tags)
        if success:
            print(f"Posted: {title}")
            save_posted_topic(title)
        else:
            print(f"Failed to post: {title}")


if __name__ == "__main__":
    main()
