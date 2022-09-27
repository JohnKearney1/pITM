# templateParser.py

# Imports
import json
import sys
from datetime import datetime


# > This method retrieves the TEMPLATE email from a json file in the script's templates folder
def loadTemplate(template, name):
    formattedSubject = ""
    formattedBody = ""
    try:
        # Open the Templates json
        f = open('data/templates/Templates.json')
        data = json.load(f)

        # Check if template exists in json
        if template in data:
            log("Using " + str(template) + " as the template")
            # use the specified template if so
            subject = data[template]['subject']
            body = data[template]['body']

        # use the default template if not
        else:
            log("Using the default template: " + str(template) + " not found")
            subject = data['default']['subject']
            body = data['default']['body']

        # If any name variables exist in the body, replace them with the name
        if body.find("{NAME}") >= 0:
            formattedBody = body.replace("{NAME}", name)
            log("Found name variables in the body, replacing them now")
        else:
            formattedBody = body

        if subject.find("{NAME}") >= 0:
            # Handle {NAME} variables
            formattedSubject = subject.replace("{NAME}", name)
            log("Found name variables in the subject, replacing them now")
        else:
            formattedSubject = subject

        f.close()

    except KeyError as e:
        log("`Templates.json` appears to be misconfigured. Check your json keys... " + str(e))
        sys.exit("\npITM > Your templates.json file looks misconfigured... Make sure you have a `subject` and a `body` "
                 "key in each template.")

    except FileNotFoundError as e:
        log("`Templates.json` is missing from the `data/templates/` directory" + str(e))
        sys.exit("\npITM > Your templates.json file is missing!")

    except json.decoder.JSONDecodeError as e:
        log("Looks like your `Templates.json` may be empty..." + str(e))
        sys.exit("\npITM > Looks like your `Templates.json` may be empty...")

    return formattedSubject, formattedBody


def loadContacts():
    # 'data/Contacts.txt'

    try:
        # Get number of lines in text file
        with open('data/Contacts.txt') as f:
            text = f.readlines()
            size = len(text)
    except FileNotFoundError as e:
        log("`Contacts.txt` is missing from the `data/` folder")
        sys.exit("\npITM > Your Contacts.txt is missing!")

    # Use that size to init a 2d array
    mailingList = [[""] * 2] * size

    x = 0
    with open('data/Contacts.txt') as f:

        try:
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

        # Can't access the email or names in Contacts.txt at startup? Tell the user then kill the program.
        except IndexError as e:
            log("The `Contacts.txt` file in `data/` is empty")
            sys.exit("\npITM > Your Contacts.txt is empty!")

    return mailingList


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
