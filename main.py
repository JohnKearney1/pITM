# PITM - @johnkearney1 @jackwlanders
# > The goal of this script is to easily automate sending
# > individualized emails to a variety of email addresses using Google SMTP servers.
import sys


def constructor():
    print("Initializing...")
    # Call authentication from here
    authenticated = auth()

    # Validate authentication from here
    if authenticated:
        print("Authenticated with Gmail...")
        print("Initialized!")
        return True

    # If authentication fails terminate the program
    if not authenticated:
        print("Authentication with Gmail >> FAIL")
        return False




def checklist():
    auth()
    getEmailList('customPath')
    fetchTemplate('templatePath')
    attachFiles('fileDir')
    writeEmail()
    sendEmail('mgmt@kearneyjohn.com', 'John', 'Subject', 'Body', 'files to attach')
    printResults()

# Authentication with Google SMTP
def auth():
    print('TODO: Use Google API to Authenticate with Gmail')
    return True

# Local file reading
def getEmailList(filePath = '/data/Contacts.xlsx'):
    print('TODO: Read in email list from excel file')

# Local file reading
# > This method retrieves the TEMPLATE email from a text file in the script's templates folder
def fetchTemplate(templatePath = '/data/templates'):
    print('TODO: Retrieve the template email from a text file and read it in as a string')

# Local file reading
# > Attaches all files from a specified directory to the email ASSUMING they are < 25mb in size
def attachFiles(fileDir = '/data/files'):
    print('TODO: Retrieve the files to send, verify they are <25mb, then store in memory to attach later')

# Runtime text formatting
# > This method formats the template email to substitute in recipient name / current date
def writeEmail():
    print('TODO: Format template retrieved from fetchTemplate')

# Client + Server Interaction
# > Sends the completed email to
def sendEmail(address, recipient, subject, body, files):
    print('TODO: Sends the email to SMTP server AND stores reciept that indicates valid or invalid delivery')

# Local file writing + text formatting
def printResults():
    print('TODO: Outputs the results of the campaign to an excel sheet')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # constructor()
    checklist()
