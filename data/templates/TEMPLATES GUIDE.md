# Templates Guide

Templates allow you to have multiple versions of emails crafted and ready to use.
At present, templates only allow you to insert the name of your recipient. 

**To insert the recipient's name , use `{NAME}` in the subject OR the body**


Templates are .json files with two keys:
`subject` and `body`  

Both are expressed as string variables, in which you can type the key `{NAME}` anywhere you want the client's name(s).

See `Template 1.json` for an example Template.

## Alternate Templates
Alternate templates have both a `subject_alt` and `body_alt` attribute IN ADDITION to the normal `subject` and `body` attributes.
Alternate templates allow you to account for missing names in email lists, by having alternate text typed out that doesn't include a name variable.

## To-Do

1. Add Date Variable
2. Add template randomization
3. Add variable customization