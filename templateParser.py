# templateParser.py

# Imports
import json

import pandas as pd


# Local file reading
# > This method retrieves the TEMPLATE email from a json file in the script's templates folder
def loadTemplate(name, template):
    # name not being provided correctly
    print("Name: " + name)

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

    mailingList = []

    with open('data/Contacts.txt') as f:
        line = f.readline()
        mailingList.append(line.split(","))


    return mailingList
