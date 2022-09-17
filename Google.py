# Google.py
# This is a modified version of the outdated `Create_Service` method found here:
# https://stackoverflow.com/questions/69252673/from-google-import-create-service-modulenotfounderror-no-module-named-google

# Imports
import pickle
import os
from datetime import datetime

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# This method triggers the oAuth 2.0 "Consent" screen
def Create_Service(*scope):

    # client_secret.json absolute path (string)
    CLIENT_SECRET_FILE = "data/auth/client_secret.json"

    # Name of the Api (string)
    API_SERVICE_NAME = "gmail"

    # v1 (string)
    API_VERSION = "v1"

    # Gmail send email scope access: https://developers.google.com/gmail/api/auth/scopes?hl=en
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    # Load a cached credentials file (pickle) if exists; if not, authenticate again
    cred = None

    pickle_file = 'data/auth/token.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print('\nGoogle > E-Mail Sending, awaiting response...')
        log("E-Mail Sending, awaiting response...")
        return service
    except Exception as e:
        print('\nGoogle > Unable to connect...')
        log("Unable to connect: " + e.__str__())
        print(e)
        return None

# Logging method
def log(text):
    # Open the log in append mode `a`
    with open('data/log.txt', 'a') as f:
        # datetime object containing current date and time
        now = datetime.now()

        # mm/dd/YY H:M:S
        dt_string = now.strftime("%H:%M:%S")

        # Write the text with the time and log message
        f.write("\n" + dt_string + " > " + text)

        # Close the file
        f.close()
