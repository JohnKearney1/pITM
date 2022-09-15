# pITM
 pITM ("Packs In The Mail") is a python email script designed for musicians and audio professionals.
 pITM uses a templating system to easily customize emails that feel personal, but can be effectively automated to reach hundreds of people at once.

**WARNING: THIS PROJECT IS A WIP USE AT YOUR OWN RISK. BUGS EXIST.**

# Overview

01 pITM/  
02 ├─ data/  
03 │  ├─ auth/  
04 │  │  ├─ client_secret.json  
05 │  │  └─ token.pickle  
06 │  ├─ files/  
07 │  ├─ templates/  
08 │  │  ├─ TEMPLATES GUIDE.md  
09 │  │  └─ Templates.json  
10 │  └─ Contacts.txt  
11 ├─ README.md  
12 ├─ DOCS.md  
13 ├─ main.py  
14 ├─ Google.py  
15 ├─ templateParser.py  
16 ├─ dependencies.txt  
17 ├─ .gitignore  
18 └─ .gitattributes  

## 01 - Root Folder

`pITM/` is the root folder of the project. All directory or file references in the script are *relative* locations
and treat this folder as the root.

## 02 - Data Folder
`data/` stores **user provided** assets the program needs to run. Templates provided.
1. `auth/`  
2. `files/`  
3. `templates/`  
4. `Contacts.txt`  

## 03 - Authorization Folder
`auth/` holds two files:
1. `client_secret.json` (user provided)
2. `token.pickle` (autogenerated)

## 04 - Client Secret (Google Developer Console)

The user must add their own (properly configured) `client_secret.json` file in this folder.
Google Developer Console (get the client_secret): https://console.developers.google.com/start/api?id=gmail.  
For info on the formatting of this file see https://developers.google.com/api-client-library/dotnet/guide/aaa_client_secrets.

The client_secret.json file is your "password" for your initial authentication flow for the Gmail API and OAuth2.
See: https://developers.google.com/gmail/api/auth/about-auth. This allows you to trigger a "consent" screen in the web browser.

## 05 - Credential Cache
`token.pickle` is autogenerated for you provided you have supplied the `client_secret.json`. 
This is a cached credential so you don't have to authenticate every single time.

## 06 - Files Folder
`files/` is a **user populated** folder that holds all the attachments to be assigned to a single email.
i.e. ALL files in this folder will be attached to EVERY email that is sent in a single run. 

**Files have a 24.5mb size limit, and can be of any type.**

## 07 - Templates
`templates/` stores two files that handle and help with crafting your emails.

## 08 - Templates Guide
`TEMPLATES GUIDE.md` is a file that explains the syntax of your templates file, and explains how to write your emails.

## 09 - Templates File
`Templates.json` is a file that holds ALL of your email templates.
A template is a preformatted message and subject that holds some variables that can be changed at runtime.
Do not delete the "default" entry, but you can add as many custom-named templates as you like (CaSE SeNsITivE).

## 10 - Contacts File
`Contacts.txt` holds the email addresses and names of everyone in your contact list arranged in the format:

`<email address>,<name>`

Enter one contact per line, no spaces, comma separated string.

## 11 - Readme
You did it!

## 12 - Docs
`DOCS.md` holds the method APIs for 
1. `main.py`
2. `Google.py`
3. `templateParser.py`

## 13 - main.py

Holds the main logic of the program, user interaction, output etc. Execute program from `main.py`:`main()`

## 14 - Google.py

Custom implementation of a Google class that creates the service necessary to send the email. 
Called from `main.py`:`sendEmail()`.

## 15 - templateParser.py

Holds the logic responsible for pulling templates, substituting in variables, and reading in the `Contacts.txt` file.

## 16 - dependencies.txt

`pip install -r dependencies.txt`

This is an incomplete list of dependencies, I haven't implemented setupTools yet for proper dependency mapping,
so you may have to debug. Sorry!

## 17 - Git Ignore (.gitignore)

GitIgnore specifies which directories and files not to pass to Git. 

In this repository, `data/auth/` is excluded for security purposes.

## 18 - Git Attributes (.gitattributes)
Autogenerated file.