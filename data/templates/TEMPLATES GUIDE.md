# Templates Guide

Templates allow you to have multiple versions of emails crafted and ready to use. Your templates are stored in the `Templates.json` file.

Templates support **variables** that allow you to substitute in client information at runtime. See below for instructions on setting up your Templates:



## Templates.json Setup

Here is the default `Templates.json` file:
> {  
>  "default": {  
>    "subject": "Default Subject",  
>    "body": "Hey!\nThe default body should not include any name variables!\nThis is because the program has to have a fallback template in the event a contact email doesn't have an associated name!\n\n- Devs\n@gawxy",  
> },  
>  "Template 1": {  
>    "subject": "Beats4{NAME}",  
>    "body": "Hey {NAME},\nI bought $6500 worth of midi files this week; let's get these beats sold!\n- Jack\n@prodlanders"  
> }  
> }  

The Templates file should ALWAYS have a key called 'default'. If no default key exists, the program may encounter errors.
You can add as many templates as you like, and the name of the template is arbitrary. For example, `"Template 1"` above could also be named `"A new teMpl8!"`. 

Each template uses two variables (everything here is a string): `subject` and `body`. You may enter any type of text and the below escape characters and variables:


### Templates.json variables

| Variable | Result                       |
|----------|------------------------------|
| `\n`     | Skips to the next line.      |
| `{NAME}` | Inserts the recipient's name |


## Templates Execution Flow

During runtime, the user is asked to specify a "template name", this is the key you'll see below at the first level of the json file.
For example, the default Templates.json allows me to enter `Template 1` or `default` or enter nothing at all.  

If nothing is entered, the `default` template is always used. If a different template (ex. Template 1) is provided the program will attempt to use that. 
If the user specified template contains variables that pITM can't find substitutions for, it will fall back to the default template. 

## Special Conditions

- If no **name** is found with a recipient's email, the program will always the `default` template. You should never put user provided (ex. {NAME}) variables in the `default` template.
