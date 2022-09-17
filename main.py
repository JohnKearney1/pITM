# main.py
# pITM - v1.1.1

# System Imports
import mimetypes
import os
import pickle
import socket
import sys
import time

# From Google (oauth 2.0 flow & requests class)
import oauthlib.oauth2.rfc6749.errors

import templateParser
from Google import Create_Service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Error handling
from googleapiclient.errors import HttpError
import httplib2.error

# Composing & encoding email
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

# Date & time
from datetime import datetime


# On startup, we clear the log.txt
def newLog():
    # Create a new log.txt or clear the existing one
    with open('data/log.txt', 'w') as f:
        # datetime object containing current date and time
        now = datetime.now()

        # mm/dd/YY H:M:S
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

        # Write the header to the file
        f.write(dt_string + " > pITM Started")

        # Close the file
        f.close()


# Writes some text to the file with the time
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


# Authentication with Google OAuth
# AUTH IS COMPLETED VIA WEB BROWSER
# > client_secret_json -> STRING : Relative location of the client_secret.json file
def auth(client_secret_json="data/auth/client_secret.json"):
    try:
        credentials = None

        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists('data/auth/token.pickle'):
            # print('pITM >> Loading credentials from cache...')
            log("Loading credentials from cache")
            # Open the pickle file (in read byte mode) and store the token under credentials
            with open('data/auth/token.pickle', 'rb') as token:
                credentials = pickle.load(token)
                log("Credentials loaded")

        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                # print('\npITM >> Refreshing access token...')
                log("Refreshing access token")
                credentials.refresh(Request())
            else:
                # print('\npITM >> Fetching new tokens...')
                log("Fetching new tokens")

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
                    # print('\npITM >> Saving credentials to cache...')
                    log("Saving credentials to cache")
                    pickle.dump(credentials, f)
                    log("Credentials saved to 'data/auth/token.pickle'")
    except oauthlib.oauth2.rfc6749.errors.AccessDeniedError as error:
        print("\npITM > Looks like you denied us access during OAuth. Without that, we can't send any emails!")
        log("User canceled authentication before it was complete")
        terminate(error)

    # Now we have our credentials (token, refresh_token, token_uri, client_id, client_seceret, scopes)
    # print(credentials.to_json())

    return credentials


# This is the logic that composes the elements of the email, this is an iterative method, you must call it from a loop.
# > index -> INT : index of the mailingList entry to search. 0 by default.
# > template -> STRING : json key string of the Template to use, uses default template by default.
# > mailingList -> STRING ARRAY (2D) : Holds the email and name of each recipient. Loads from Contacts.txt by default.
def composeMail(index=0, template="default", mailingList=templateParser.loadContacts()):
    # mailingList[index][0] == email addr
    # mailingList[index][1] == name
    # mailingList[index] == ['<email>', '<name>']

    # If recipient has an email AND a name entry use this template
    if len(mailingList[index]) > 1:
        # Load a custom template for the current recipient
        subject, body = templateParser.loadTemplate(name=mailingList[index][1], template=template)

    # Otherwise use this template
    else:
        subject, body = templateParser.loadTemplate(template=template)

    # Tell the user what the email looks like:
    print("\nEmail No." + (index + 1).__str__())
    log("Email No." + (index + 1).__str__())

    # If the mailing list includes a name for this entry print the name of the recipient
    if len(mailingList[index]) > 1:
        print("Name: " + mailingList[index][1])
        log("Name: " + mailingList[index][1])

    # Otherwise, print that we don't know the name
    else:
        print("Name: Unknown")
        log("Name: Unknown")

    # Print the rest of the information
    print("E-Mail: " + mailingList[index][0])
    log("E-Mail: " + mailingList[index][0])
    print("Subject: " + subject)
    log("Subject: " + subject)
    print("Body: " + body)
    log("Body: \n\n" + body + "\n\n")

    return subject, body


# Returns a list of the files inside of a directory (`data/files` by default) with
# fileDir -> STRING : Directory of files to attach to each email
def getFiles(fileDir="data/files"):
    fileList = []

    for item in os.listdir(fileDir):
        fileList.append(fileDir + '/' + item)

    return fileList


# USAGE LIMITS: https://developers.google.com/gmail/api/reference/quota?hl=en
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
                log("Uploading " + attachment.__str__())
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
                log("File `" + attachment + "` skipped")
                print("\npITM > File `" + attachment + "` skipped")

        # Save the raw string
        raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

        print("\npITM > Files attached...")
        log("Files attached")

        # Sends the email using 'me' as the authenticated account
        response = service.users().messages().send(
            userId='me',
            body={'raw': raw_string}
        ).execute()

        print("\nRESPONSE > " + str(response))
        log("Response: " + str(response))

    except HttpError as error:
        log("HttpError triggered")
        terminate(error)

    except socket.gaierror and httplib2.error.ServerNotFoundError as error:
        print(F'\npITM > Is the internet off? {error}')
        log("Is the internet off? Socket or ServerNotFound error triggered")
        if input("Press `q` to quit, or enter to try again: ") == 'q':
            terminate(error)


# Main method
def main():
    # Authenticate on startup and store the credential token in `data/auth/token.pickle`
    try:
        auth()
    except FileNotFoundError as e:
        print("\npITM > Your client_secret.json file is missing!")
        log("The client_secret.json file wasn't found in 'data/auth' ")
        terminate(e)

    # Get the template ID from the user
    templateID = input("\npITM > Enter the name of the template to use, or press enter to use the default template: ")
    log("User specified `templateID`: " + templateID)

    # If nothing specified, template is set to default
    if templateID is None or "":
        templateID = "default"
        log("Using default template")

    # ISSUE 3: https://github.com/JohnKearney1/pITM/issues/3
    # load the contacts, done in main so we only do this once
    mailingList = templateParser.loadContacts()

    print("\n======== Mailing List ========")
    log("======== Mailing List ========")

    x = 1
    for recipient in mailingList:
        log(recipient.__str__())
        print(x.__str__() + "] " + recipient.__str__())
        x = x + 1

    _, _ = composeMail(index=0, template=templateID, mailingList=mailingList)

    log("THE ABOVE IS AN EXAMPLE EMAIL - IT WAS NOT SENT")

    # Allow user to confirm sends
    lastChance = input("\npITM > This is an example email.\n\npITM > Look good? Press enter to send or q "
                       "to quit: ")

    if lastChance.lower() == "q":
        log("User chose to terminate the program")
        terminate(None)

    log("User approved template email, sending all emails now")

    index = 0
    for recipient in mailingList:
        # Feed info into the templating engine to write the email
        subject, body = composeMail(index=index, template=templateID, mailingList=mailingList)

        # Pause execution to ensure we don't exceed rate limits (usually not an issue, this is just a safeguard)
        time.sleep(0.75)

        # Upload the attachments and send the email
        sendEmail(recipientEmail=recipient[0], subject=subject, body=body,
                  files=getFiles("data/files"))

        # Iterate index
        index = index + 1


# Kills the program and prints an error if one is provided
# > error -> OBJ : Denotes that the exit is an error, obj holds error information.
# > error -> None : Denotes that the exit is intentional.
def terminate(error):
    if error is not None:
        log("Error: " + error.__str__())
        sys.exit("\npITM > Error: " + error.__str__())

    else:
        log("Exiting")
        sys.exit("\npITM > Exiting...")


# Press the green button in the gutter to run the script
if __name__ == '__main__':
    try:

        # Generate a new log.txt
        newLog()

        # Run the main logic
        main()

        # When main logic finishes, say goodbye & terminate with no errors!
        print("\npITM > Finished!")
        log("Finished!")
        terminate(None)

    # If user force stops program print this:
    except KeyboardInterrupt as e:
        print("\n\npITM > Execution Halted")
        log("Execution Halted: " + str(e))
