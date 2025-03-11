# import re
# import webbrowser
# import time
# import os
# from google_apis import create_service

# CLIENT_FILE = "/Users/anthonycano-luna/Downloads/anthony-dejunkacct1.json"
# API_NAME = 'gmail'
# API_VERSION = "v1"
# SCOPES = ['https://mail.google.com/']

# gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

# # Set a limit on how many tabs so we do not crash the system
# MAX_TABS_OPEN = 3

# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"))


# def search_unsubscribe_emails(query_string, labels=None):
#     '''
#     Based off of the search_emails function in delete.py. Modified to find
#     emails with an unsubcribe link in the body.
#     '''
#     result = gmail_service.users().messages().list(
#         userId='me',
#         q=query_string
#     ).execute()

#     return result.get('messages', [])

# #Hard coded query for testing
# query_string = '"unsubscribe" AND category:promotions AND newer_than:90d AND from:ticketmaster.com'

# email_results = search_unsubscribe_emails(query_string)
# print(email_results)

# def extract_link(email_id):
#     """Extract the List-Unsubscribe link from an email's headers."""
#     message_info = gmail_service.users().messages().get(userId='me', id=email_id).execute()

#     for header in message_info.get('payload', {}).get('headers', []):
#         if header.get('name') == 'List-Unsubscribe':
#             url_match = re.findall(r'<(.*?)>', header.get('value'))
#             if url_match:
#                 return url_match[0]  # Return first found URL
#     return None


# def open_unsubscribe_links():
#     email_results = search_unsubscribe_emails(query_string)
#     # To avoid duplicate links (if you get multiple emails from the same sender)
#     seen_urls = set()
#     curr_open = 0

#     for email in email_results:
#         email_id = email['id']
#         unsubscribe_url = extract_link(email_id)


#         # Just validating the url

#         if unsubscribe_url and unsubscribe_url.startswith("http"):
#             base_url_match = re.findall(r'(.*?\.(com|edu|net|gov))', unsubscribe_url)
#             if base_url_match:
#                 base_url = base_url_match[0][0]  # Get the domain
#                 if base_url not in seen_urls: # If we havent seen it before
#                     print(f"Opening: {unsubscribe_url}")
#                     webbrowser.get('chrome').open(unsubscribe_url)
#                     seen_urls.add(base_url)
#                     curr_open += 1

#         # Limit tabs opened at a time
#         if curr_open >= MAX_TABS_OPEN:
#             answer = input('Opened 3 tabs. Type "yes" to continue or "no" to stop: ')
#             if answer.lower() == "yes":
#                 curr_open = 0  # Reset counter
#             else:
#                 break

# open_unsubscribe_links()


import re
import webbrowser
import os
from google_apis import create_service

# === GMAIL API CONFIGURATION ===
CLIENT_FILE = "/Users/anthonycano-luna/Downloads/anthony-dejunkacct1.json"
API_NAME = 'gmail'
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']

# Create Gmail service
gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

# Set a limit on how many tabs to avoid system overload
MAX_TABS_OPEN = 3

# Register Chrome for opening unsubscribe links
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"))


def search_unsubscribe_emails(query_string):
    """Search for emails with unsubscribe links."""
    result = gmail_service.users().messages().list(
        userId='me',
        q=query_string
    ).execute()

    return result.get('messages', [])


def extract_link(email_id):
    """Extract the List-Unsubscribe link from an email's headers."""
    message_info = gmail_service.users().messages().get(userId='me', id=email_id).execute()

    # ✅ FIX: Properly access headers
    headers = message_info.get('payload', {}).get('headers', [])

    for header in headers:
        if header.get('name').lower() == 'list-unsubscribe':
            url_match = re.findall(r'<(.*?)>', header.get('value'))
            if url_match:
                return url_match[0]  # ✅ Return first found URL

    return None


def open_unsubscribe_links():
    """Find, extract, and open unsubscribe links with a limit."""
    # ✅ Define query_string inside the function
    query_string = '"unsubscribe" AND category:promotions AND newer_than:90d AND from:ticketmaster.com'
    email_results = search_unsubscribe_emails(query_string)

    seen_urls = set()  # Avoid duplicate links
    curr_open = 0  # Track tabs opened

    if not email_results:
        print("No emails found matching the query.")
        return

    for email in email_results:
        email_id = email['id']
        unsubscribe_url = extract_link(email_id)

        if unsubscribe_url:
            # ✅ Ensure valid HTTP link
            if unsubscribe_url.startswith("http"):
                base_url_match = re.findall(r'(.*?\.(com|edu|net|gov))', unsubscribe_url)
                if base_url_match:
                    base_url = base_url_match[0][0]  # Get domain
                    if base_url not in seen_urls:  # Avoid duplicates
                        print(f"Opening: {unsubscribe_url}")
                        webbrowser.get('chrome').open(unsubscribe_url)
                        seen_urls.add(base_url)
                        curr_open += 1
            else:
                print(f"Skipping non-http unsubscribe link: {unsubscribe_url}")

        # ✅ LIMIT OPEN TABS
        if curr_open >= MAX_TABS_OPEN:
            answer = input("Opened 3 tabs. Type 'yes' to continue or 'no' to stop: ")
            if answer.lower() == 'yes':
                curr_open = 0
            else:
                break


# === RUN THE SCRIPT ===
open_unsubscribe_links()
