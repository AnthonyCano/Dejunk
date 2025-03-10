import re
import webbrowser
import time
import os
from google_apis import create_service

CLIENT_FILE = "/Users/anthonycano-luna/Downloads/anthony-dejunkacct1.json"
API_NAME = 'gmail'
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']

gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

# Set a limit on how many tabs so we do not crash the system
MAX_TABS_OPEN = 3

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"))


def search_unsubscribe_emails(query_string, labels=None):
    '''
    Based off of the search_emails function in delete.py. Modified to find
    emails with an unsubcribe link in the body.
    '''
    result = gmail_service.users().messages().list(
        userId='me',
        q=query_string
    ).execute()

    return result.get('messages', [])

#Hard coded query for testing
query_string = '"unsubscribe" AND category:promotions AND newer_than:90d AND from:ticketmaster.com'

email_results = search_unsubscribe_emails(query_string)
print(email_results)
