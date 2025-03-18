import re
import webbrowser
import time
import os
from delete import search_emails
from google_apis import create_service

CLIENT_FILE = "/Users/anthonycano-luna/Downloads/anthony-dejunkacct1.json"
API_NAME = 'gmail'
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']

gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

# Set a limit on how many tabs so we do not crash the system
MAX_TABS_OPEN = 3

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"))


def get_user_input():
    '''
    Function to get the information of the email sender that the user would like to unsubscribe from.
    Returns: The querey string that will then be used to search for.
    '''

    # For now I just want to be able to use the default gmail categories
    valid_categories = ["primary", "promotions", "social", "updates", "forums"]
    
    while True:
        # Get and validate category
        input_category = input("Please enter the email category you want to unsubscribe from (e.g., promotions): ").strip().lower()
        if input_category not in valid_categories:
            print(f"You selected '{input_category}', which is not a valid category.")
            print("Please select from one of the five valid categories: primary, promotions, social, updates, forums.")
            continue  # Restart from category input
        

        while True:
            input_sender = input("Please enter the company name or sender you want to unsubscribe from (e.g., Dejunk): ").strip()

            if not input_sender:
                print("Sender cannot be empty. Please enter a valid sender.")
                continue  
            
            if "from" in input_sender.lower():
                print(f"You entered '{input_sender}'. Please ensure you only enter the sender name (e.g., 'Dejunk').")
                continue  
            
            break  # Valid sender input, exit sender loop

        # Construct the query string
        full_string = f"category:{input_category} from:{input_sender}"
        print(f"You will now unsubscribe from: {full_string}.")
        
        ans = input("If this is correct, please type 'yes': ").strip().lower()
        if ans == "yes":
            return full_string
        else:
            print("Restarting process...\n")  # Allow retrying without exiting

get_user_input()

# Hard coded query for testing
query_string = '"unsubscribe" AND category:promotions AND newer_than:90d AND from:ticketmaster.com'

# Call the search function in the delete script to fetch the email ids
# that match the query_string
email_results = search_emails(query_string)
print(email_results)


