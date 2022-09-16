# templateParser.py

# Imports
import json

import pandas as pd


# Local file reading
# > This method retrieves the TEMPLATE email from a json file in the script's templates folder
def loadTemplate(name, template):

    # Open the Templates json
    f = open('data/templates/Templates.json')
    data = json.load(f)

    # Check if template exists in json
    if template in data:
        # use the specified template if so
        subject = data[template]['subject']
        body = data[template]['body']
    else:
        # use the specified template if so
        subject = data['default']['subject']
        body = data['default']['body']

    # Handle {NAME} variables
    formattedSubject = subject.replace("{NAME}", name)
    formattedBody = body.replace("{NAME}", name)

    return formattedSubject, formattedBody


def loadContacts():
    # 'data/Contacts.txt'

    # Get number of lines in text file
    with open('data/Contacts.txt') as f:
        text = f.readlines()
        size = len(text)

    # Use that size to init a 2d array
    mailingList = [[""]*2]*size

    x = 0
    with open('data/Contacts.txt') as f:
        nextLine = True
        while nextLine:
            # Read the first line and split into 2 substrings: email & name
            line = f.readline()
            substring = line.split(" ")

            # Remove \n (new line) escape code
            substring[0] = substring[0].replace('\n', '')
            substring[1] = substring[1].replace('\n', '')

            # Set the substring list to the current iter of our mailingList
            mailingList[x] = substring

            # Iterate & ensure we haven't read all the lines in the file yet, if we have then break
            x = x + 1
            if x >= size:
                nextLine = False

    print(mailingList)

    return mailingList
