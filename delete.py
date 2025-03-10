import time
from google_apis import create_service

CLIENT_FILE = "client-secrect.json"
API_NAME = 'gmail'
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']

gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

# Search through emails
def search_emails(query, labels=None):
    return