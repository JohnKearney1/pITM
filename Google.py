# Google.py
# This is a modified version of the outdated `Create_Service` method found here:
# https://stackoverflow.com/questions/69252673/from-google-import-create-service-modulenotfounderror-no-module-named-google

# Imports
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
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
    print(SCOPES)

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
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
