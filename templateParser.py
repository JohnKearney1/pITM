# templateParser.py

# Imports
import json

import pandas as pd


# Local file reading
# > This method retrieves the TEMPLATE email from a json file in the script's templates folder
def loadTemplate(template, name="ALTERNATE_TEMPLATE"):
    formattedSubject = ""
    formattedBody = ""

    if name != "ALTERNATE_TEMPLATE":
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

        if body.find("{NAME}") >= 0:
            formattedBody = body.replace("{NAME}", name)

        if subject.find("{NAME}") >= 0:
            # Handle {NAME} variables
            formattedSubject = subject.replace("{NAME}", name)

        f.close()

    else:
        f = open('data/templates/Templates.json')
        data = json.load(f)

        # use the specified template if so
        subject = data['default']['subject']
        body = data['default']['body']

        f.close()

        formattedSubject = subject
        formattedBody = body

    return formattedSubject, formattedBody


def loadContacts():
    # 'data/Contacts.txt'

    # Get number of lines in text file
    with open('data/Contacts.txt') as f:
        text = f.readlines()
        size = len(text)

    # Use that size to init a 2d array
    mailingList = [[""] * 2] * size

    x = 0
    y = 0
    with open('data/Contacts.txt') as f:
        nextLine = True
        while nextLine:
            # Read the first line and split into 2 substrings: email & name
            line = f.readline()

            # print(line)
            substring = line.split(" ")

            # print(substring)

            # Remove \n (new line) escape code
            substring[0] = substring[0].replace('\n', '')

            if len(substring) > 1:
                # Remove \n (new line) escape code
                substring[1] = substring[1].replace('\n', '')

                # Set the substring list to the current iter of our mailingList

            mailingList[x] = substring

            # Iterate & ensure we haven't read all the lines in the file yet, if we have then break
            x = x + 1
            if x >= size:
                nextLine = False

    # print(mailingList)

    return mailingList
