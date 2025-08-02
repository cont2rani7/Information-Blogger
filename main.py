import logging
from fetch_trending_topics import get_trending_topics
from generate_content import generate_blog_content
from tagging_and_category import detect_category_and_tags
from post_to_blogger import post_blog
from tracker import is_duplicate, save_posted_topic

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in environment variables.")
logging.basicConfig(level=logging.INFO)

def main():
    topics = get_trending_topics()
    if not topics:
        logging.info("No trending topics found.")
        return

    for topic in topics:
        title = topic["title"]
        if is_duplicate(title):
            logging.info(f"Skipping duplicate: {title}")
            continue

        try:
            blog_data = generate_blog_content(title, GEMINI_API_KEY)
            content = blog_data['content']
            category = blog_data['category']
            tags = blog_data['tags']

            success = post_blog(blog_data['title'], content, category, tags)
            if success:
                logging.info(f"Posted: {title}")
                save_posted_topic(title)
            else:
                logging.error(f"Failed to post: {title}")
        except Exception as e:
            logging.exception(f"Error processing topic '{title}': {e}")

if __name__ == "__main__":
    main()
