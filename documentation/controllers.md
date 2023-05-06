## Controllers
Every non-dialog window is held inside StackedWidget. There are $$$ windows, depending on the settings used, some of them might be skipped.

#### Main windows

- **Drop** - user can drag&drop his folder/files or use the choose button to select input files (files only, folder input is not supported here - limitation of PyQt). Toggle button switches between auto mode and manual mode of cutout process. When nn is loading or output folder doesn't exist the relevant message is going to be shown.
- **Progress** - this window is shown during every processing of image (drop &rarr; main, main &rarr; main/end/sim)
- **Data** - Displays found cutouts and input image, by clicking on the cutout itself, a dialog will show the detailed view on cutout
 user can use buttons next to every cutout to:
  - toggle cutout on/off if he doesn't want it to be saved
  - rotate cutout
  - edit the area and location of cutout (Edit)

  Next button processes the next image in queue. Auto starts the auto mode (same as enabling auto mode toggle on Drop).
- **Similarity (Sim)** - similar to Data, but for duplicity. Displays cutouts that are more similar than threshold. Buttons next to duplicities are:
  - set this image as the main image and load its duplicities
  - toggle on/off

  Accept keeps the main cutout, Decline deletes it (both will also remove toggled duplicities), Accept all skips duplicity detection and keeps all of them (same as disabling duplicity detection in settings).
- **End** - final screen after finishing all steps for all the inputs.

#### Other windows and dialogs
- **Edit** - Allows changes in the cut area. This is the only window being build for every edit operation again, which might not be the ideal way, but it was the easiest way to implement at that time. User can select the area using the SelectionBox or by using the select points button.
- **About** - Dialog with basic info about the app.
- **Settings** - Dialog that allows user to change following settings:
  - Output image format
  - Output folder - where will the projects' subfolders with cutouts be located
  - Duplicity detection - sets if duplicity detection (Sim) will be used
  - Fix rotation using AI - enables/disables usage of nn. If nn is not loaded yet and this sett. is turn on then message will be displayed on Drop during nn loading.
  - Language - changes translation of the app (allows to restart the app for change)
- **Popup dialog** - universal dialog used for ensuring questioning of user