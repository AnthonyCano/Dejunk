import time
from google_apis import create_service

# File path for the tester email. This is just a general file path for now
# After I make sure everything works this test key will be deleted and I 
# will figure out how to securely store and hide this info!
CLIENT_FILE = "/Users/anthonycano-luna/Downloads/anthony-dejunkacct1.json"
API_NAME = 'gmail'
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']

gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

def search_emails(query, labels=None):
    # email_messages = []
    next_page_token = None
    
    message_response = gmail_service.users().messages().list(
        userId='me',
        labelIds=labels,
        includeSpamTrash=False,
        q=query,
        maxResults=500
    ).execute()
    email_messages = message_response.get('messages')
    next_page_token = message_response.get('nextPageToken')

    while next_page_token:
        message_response = gmail_service.users().messages().list(
            userId='me',
            labelIds=labels,
            q=query,
            maxResults=500,
            includeSpamTrash=False,
            pageToken=next_page_token
        ).execute()
        email_messages.extend(message_response['messages'])
        next_page_token = message_response.get('nextPageToken')
        print('Page Token: {0}'.format(next_page_token))
        time.sleep(0.5)
    return email_messages

query_string = "category:promotions "
email_results = search_emails(query_string)
print(email_results)

# Now that we have our id's for the emails we want to delete
# we can just used Googles built in methods to get rid of the emails!

for email_result in email_results:
    gmail_service.users().messages().trash(
        userId='me',
        id=email_result['id']
    ).execute()