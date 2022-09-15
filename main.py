# main.py
# PITM - @johnkearney1
# > The goal of this script is to easily automate sending
# > individualized emails to a variety of email addresses using Google SMTP servers.

# Imports
import mimetypes
import os
import pathlib
import pickle

# From google (oauth 2.0 flow & requests class)
import sys
import time

import Google
import templateParser
from Google import Create_Service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Composing & encoding email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

# FIELD VARIABLES
from googleapiclient.errors import HttpError

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'data/auth/client_secret.json'
APPLICATION_NAME = 'pITM-01'


# Authentication with Google SMTP
# AUTH IS COMPLETED VIA WEB BROWSER
def auth(client_secret_json="data/auth/client_secret.json"):
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('data/auth/token.pickle'):
        print('AUTH >> Loading Credentials From File')
        # Open the pickle file (in read byte mode) and store the token under credentials
        with open('data/auth/token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('AUTH >> Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('AUTH >> Fetching New Tokens')

            # Create a flow object & Define the scope of the information our script can access
            # We would define our client_secret_json location here, but the default location is in the params
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/auth/client_secret.json',
                scopes=[
                    'https://www.googleapis.com/auth/gmail.send'
                ]
            )

            # Create a local server to run the oAuth consent screen
            # The second parameter `prompt` is set so that we ALWAYS get a refresh token back from oAuth
            flow.run_local_server(port=8080, prompt='consent')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('data/auth/token.pickle', 'wb') as f:
                print('AUTH >> Saving Credentials for Future Use')
                pickle.dump(credentials, f)

    # Now we have our credentials (token, refresh_token, token_uri, client_id, client_seceret, scopes)
    # print(credentials.to_json())

    return credentials


def composeMail(template):
    # This loops the logic that sends the email
    # USAGE LIMITS: https://developers.google.com/gmail/api/reference/quota?hl=en

    mailingList = templateParser.loadContacts()

    # We will compose and format our email within the for loop, so we don't have to store every variation in a variable
    x = 0
    for recipient in mailingList:
        # recipient[0] == email addr
        # recipient[1] == name

        # Load a custom template for the current recipient
        subject, body = templateParser.loadTemplate(recipient[1], template)

        # Pause execution for 2 seconds to ensure we don't exceed rate limits
        time.sleep(2)
        sendEmail(recipientEmail=recipient[0], subject=subject, body=body,
                  files=getFiles("data/files"))
        # C:/Users/kearn/OneDrive/Desktop/pITM/
        x = x + 1


# Local file reading
# > Attaches all files from a specified directory to the email
def getFiles(fileDir):
    fileList = []

    for item in os.listdir(fileDir):
        fileList.append(fileDir + '/' + item)

    print(fileList)
    return fileList


# Client + Server Interaction
# > recipientEmail -> STRING : Email address of the intended recipient
# > subject -> STRING : Subject line of the email
# > body -> STRING : Main content of the email
# > files -> STRING ARRAY : Array containing the relative locations of the files to attach as strings
def sendEmail(recipientEmail, subject, body, files):
    try:

        service = Create_Service()
        # service = build('gmail', 'v1', credentials=auth())
        # Create a new EmailMessage object
        message = MIMEMultipart()

        # Add our data to it
        message['To'] = recipientEmail
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Attach files
        for attachment in files:
            if os.path.getsize(attachment) < 24500000:
                # Guess the mimetype
                content_type, encoding = mimetypes.guess_type(attachment)
                main_type, sub_type = content_type.split('/', 1)
                file_name = os.path.basename(attachment)

                # open attachment as binary
                f = open(attachment, 'rb')

                # read the file in and encode it
                myFile = MIMEBase(main_type, sub_type)
                myFile.set_payload(f.read())
                myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
                encoders.encode_base64(myFile)

                # close the filereader
                f.close()

                # attach the file to the email
                message.attach(myFile)

            else:
                print("File " + attachment + " too large... Skipping.")

        # Save the raw string
        raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Sends the email using 'me' as the authenticated account
        response = service.users().messages().send(
            userId='me',
            body={'raw': raw_string}
        ).execute()

        print(response)

    except HttpError as error:
        print(F'An error occurred: {error}')


def main():
    # Authenticate on startup and store the credential token in `data/auth/token.pickle`
    print("STARTUP >> Initializing Google oAuth 2.0")
    auth()
    print("STARTUP >> Authenticated")

    # Get the template ID from the user
    templateID = input("Enter the name of the template to use, or leave blank to use the default template: ")
    if templateID is None or "":
        # If nothing specified, first template is default
        templateID = "default"

    # Allow user to confirm sends
    lastChance = input("Ready to send? Press enter. To quit, type q: ")
    if lastChance.lower() == "q":
        print("Exiting...")
        sys.exit(0)

    # Send the emails
    composeMail(template=templateID)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
