# PicScan

App for cutting photos out of scanned images, includes rotation correction and duplicity detection.

### About
We made this app as a project for our subjects RPR1/RPR2. It should be an opensource alternative to other similarly functioning software. \

Our assignment was:
- App takes folder or files as an input
- Every file is processed (photo detection) and results are displayed as a separate pieces
- App automatically detects photo's rotation and cuts it out, both of these properties can  be edited by user before saving
- App checks for photo duplicities

### Built mainly thanks to
PyCharm, GitHub, JIRA, PyQt5, TensorFlow, OpenCV

### Steps to run this project
1. Python (3.10 recommended)

    we recommend to create venv:
   - PyCharm: `Add New Interpreter -> Add Local Interpreter -> Virtualenv Envirnoment -> New -> [path]/venv`
   - Cmd: `python  -m venv [path]/venv`
2. Clone repository
3. Install requirements \
   (if using venv, activate it first: `[path]/venv/Scripts/activate`)\
`pip install -r requirements.txt`
4. Run main.py

- To build the app run: `pyinstaller main.spec`\
output directory will be located in the "dist"

### Structure
The app is structured into three main layers:
- [Controllers](documentation/controllers.md) - UI control, every window and dialog has its own
- [Managers](documentation/controllers.md) - core functionalities
- Utils - supporting functions for managers and controllers