import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

SCOPES = ["https://www.googleapis.com/auth/blogger"]

BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID')
CREDENTIALS_JSON = os.getenv('CREDENTIALS_JSON')
if not BLOGGER_BLOG_ID or not CREDENTIALS_JSON:
    raise ValueError("BLOGGER_BLOG_ID must be set in environment variables.")

def get_blogger_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('CREDENTIALS_JSON', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("blogger", "v3", credentials=creds)
    return service


def post_blog(title, content, category, tags):
    service = get_blogger_service()
    blog_id = BLOGGER_BLOG_ID  # Replace with your actual blog ID
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