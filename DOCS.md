# PITM v2.0 Docs


## `Pitm.py`

### terminate() -> VOID

Kills the program with an error message.


| Param | Type                      |
|-------|---------------------------|
| error | Caught Exception (Object) |
| error | None                      |

### newLog() -> VOID

Generates a new `log.txt` or wipes the existing file.
 
There are no parameters for this method.

### log() -> VOID

Adds the given line of text to the `log.txt` file.

| Param | Type   |
|-------|--------|
| text  | String |

### loadTemplate() -> formattedSubject, formattedBody

Retrieves the template email from a json file in the `templates` folder.

| Param    | Type   | Default Value | Required |
|----------|--------|---------------|----------|
| template | String | N/A           | Yes      |
| name     | String | N/A           | Yes      |

| Returns          | Type   | Description                                                   |
|------------------|--------|---------------------------------------------------------------|
| formattedSubject | String | Returns the subject with any variables already substituted in |
| formattedBody    | String | Returns the body with any variables already substituted in    |




### loadContacts() -> mailingList

Gets the mailingList from `data/Contacts.txt` and returns it as a 2d Array

| Returns     | Type               | Description |
|-------------|--------------------|--------|
| mailingList | String Array (2d)  |        |


### eatPickle()

Destroys the cached pickle credential so a new one can be generated.


### auth()

Triggers the OAuth consent screen at startup, or verifies the token integrity and authenticates.

No client_secret_json param needs to be provided unless you've moved the default location.

| Param              | Type     |
|--------------------|----------|
| client_secret_json | String   |
| client_secret_json | `default`  |


### composeMail()

Compose mail formats the template text into the necessary components of the final email.

| Param       | Type              | Default Value  | Required |
|-------------|-------------------|----------------|----------|
| index       | int               | 0              | No       |
| template    | String            | "default"      | No       |
| mailingList | String Array (2d) | loadContacts() | No       |

### getFiles()

Creates a list of all the filepaths for every file in a given folder.

| Param   | Type   | Default Value | Required |
|---------|--------|---------------|----------|
| fileDir | String | "data/files"  | No       |

### sendEmail()

Combines elements of the written email to encode the data, upload attachments, and send the email to Gmail API.

| Param          | Type   | Default Value | Required |
|----------------|--------|---------------|----------|
| recipientEmail | String | N/A           | Yes      |
| subject        | String | N/A           | Yes      |
| body           | String | N/A           | Yes      |
| files          | String | N/A           | Yes      |

