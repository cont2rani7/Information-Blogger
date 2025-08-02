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