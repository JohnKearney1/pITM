## Release Notes v2.0.0

- Updated `.gitIgnore`
- Combined `main.py` and `templateParser.py` into a single file: `Pitm.py`
- Fixed `.py` file naming conventions
- Wrote updated `DOCS.md`
- 

## Release Notes - v1.2.0
This version focuses on small bug fixes and a slight re-organization of the repository in preparation for larger changes in upcoming versions.

## Release Notes - v1.1.0
This version focuses primarily on error handling and logging. I've added logging methods to all three python files to
print verbose output to `data/log.txt`.

You can log something like this: `log("This will appear in the log with a timestamp!")`

I've also surrounded a good majority of the code in exception handling blocks with log output to help debug issues.
Missing or misconfigured files, connection errors and more are all handled with this update although as more execution
flow possibilities are discovered more may be added.

I've also updated the templates guide, Readme (duh), and added an example client_secret file for dev purposes.
No API keys are in the example file.

The `data/files/` folder now has some extra logic to skip over any files that begin with a `.` to prevent hidden directories
from being accidentally attached. There are two included test files for dev purposes.
DO NOT keep any files you DO NOT want attached in this folder during actual usage.