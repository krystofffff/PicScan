# PicScan
Annual project for 7RPR1, 7RPR2

## Assignment
- App takes folder or files as an input
- Every file is processed (photo detection) and results are displayed as a separate pieces
- App automatically detects photo's rotation and cuts it out, both of these properties can  be edited by user before saving
- App checks for photo duplicities

### How to initialize project:
0. Preconditions: Python 3.10, Recommended: PyCharm
1. Create venv in project
   - PyCharm: `Add New Interpreter -> Add Local Interpreter -> Virtualenv Envirnoment -> New -> [path]/venv`
   - Cmd: `python  -m venv [path]/venv`
2. Install libraries:
   - PyCharm: `pip install -r [path]/requirements.txt`
   - Cmd: `Activate venv first: [path]/venv/Scripts/activate, then proceed with PyCharm variant`

### Building app:
- `pyinstaller main.spec`
   