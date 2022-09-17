# main.py
# pITM - @johnkearney1
# > The goal of this script is to easily automate sending
# > individualized emails to a variety of email addresses using Google SMTP servers & OAuth2.

# System Imports
import mimetypes
import os
import pickle
import socket
import sys
import time

# From Google (oauth 2.0 flow & requests class)
import templateParser
from Google import Create_Service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Error handling
from googleapiclient.errors import HttpError
import httplib2.error

# Composing & encoding email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

# FIELD VARIABLES
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'data/auth/client_secret.json'
APPLICATION_NAME = 'pITM-01'


# Authentication with Google SMTP
# AUTH IS COMPLETED VIA WEB BROWSER
def auth(client_secret_json="data/auth/client_secret.json"):
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('data/auth/token.pickle'):
        print('pITM >> Loading Credentials From File')
        # Open the pickle file (in read byte mode) and store the token under credentials
        with open('data/auth/token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('pITM >> Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('pITM >> Fetching New Tokens')

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
                print('pITM >> Saving Credentials for Future Use')
                pickle.dump(credentials, f)

    # Now we have our credentials (token, refresh_token, token_uri, client_id, client_seceret, scopes)
    # print(credentials.to_json())

    return credentials


def composeMail(template="default"):
    # This loops the logic that sends the email
    # USAGE LIMITS: https://developers.google.com/gmail/api/reference/quota?hl=en
    mailingList = templateParser.loadContacts()
    x = 1
    print("\n======== Mailing List ========")
    for recipient in mailingList:
        print(x.__str__() + "] " + recipient.__str__())
        x = x + 1

    # Allow user to confirm sends
    lastChance = input("\n\npITM > Ready to send? Press enter to send or q to quit: ")
    if lastChance.lower() == "q":
        print("pITM > Exiting...")
        sys.exit(0)

    # We will compose and format our email within the for loop, so we don't have to store every variation in a variable
    x = 0
    for recipient in mailingList:
        # recipient[0] == email addr
        # recipient[1] == name

        # print(recipient)
        # If recipient has an email AND a name entry use this template
        if len(recipient) > 1:
            # Load a custom template for the current recipient
            subject, body = templateParser.loadTemplate(name=mailingList[x][1], template=template)

        # Otherwise use this template
        else:
            subject, body = templateParser.loadTemplate(template=template)



        print("\n\nSending Email No." + (x + 1).__str__())

        if len(recipient) > 1:
            print("To: " + recipient[1])
        else:
            print("To: <NO NAME SPECIFIED>")

        print("E-Mail Addr: " + recipient[0])
        print("Subject: " + subject)
        print("Body: " + body)


        # Pause execution for 0.6 seconds to ensure we don't exceed rate limits
        time.sleep(0.6)
        sendEmail(recipientEmail=recipient[0], subject=subject, body=body,
                  files=getFiles("data/files"))
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

        main_type = ""
        sub_type = ""

        # Attach files
        for attachment in files:
            if os.path.getsize(attachment) < 24550000 and attachment.__str__()[0:12] != "data/files/.":
                # Guess the mimetype
                content_type, encoding = mimetypes.guess_type(attachment)
                if content_type is None or encoding is not None:

                    content_type = 'application/octet-stream'

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
                print("\npITM > File " + attachment + " skipped...")

        # Save the raw string
        raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Sends the email using 'me' as the authenticated account
        response = service.users().messages().send(
            userId='me',
            body={'raw': raw_string}
        ).execute()



        print("\nRESPONSE > " + str(response))

    except HttpError as error:
        print(F'An error occurred: {error}')

    except socket.gaierror and httplib2.error.ServerNotFoundError as error:
        print(F'\nIs the internet is off? {error}')
        if input("Press `q` to quit, or enter to try again: ") == 'q':
            sys.exit(0)



def main():
    # Authenticate on startup and store the credential token in `data/auth/token.pickle`
    auth()

    # Get the template ID from the user
    templateID = input("pITM > Enter the name of the template to use, or press enter to use the default template: ")

    # If nothing specified, template is set to default
    if templateID is None or "":
        templateID = "default"

    # Compose the emails
    composeMail(template=templateID)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
