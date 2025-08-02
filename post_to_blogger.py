import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import json
import io

SCOPES = ["https://www.googleapis.com/auth/blogger"]

BLOG_ID = os.getenv("BLOG_ID")  # Default to a sample blog ID if not set
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

def get_blogger_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_json = os.getenv("GOOGLE_CREDENTIALS")
            if not credentials_json:
                raise Exception("GOOGLE_CREDENTIALS environment variable not set.")
            creds_dict = json.loads(credentials_json)
            creds_io = io.StringIO(json.dumps(creds_dict))
            flow = InstalledAppFlow.from_client_secrets_file(creds_io, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("blogger", "v3", credentials=creds)
    return service


def post_blog(title, content, category, tags):
    service = get_blogger_service()
    blog_id = BLOG_ID  # Replace with your actual blog ID
    post = {
        "kind": "blogger#post",
        "title": title,
        "labels": tags,
        "content": content,
        category: category if category else None,
        "status": "live"
    }
    try:
        service.posts().insert(blogId=blog_id, body=post).execute()
        return True
    except Exception as e:
        print("Failed to post:", e)
        return False