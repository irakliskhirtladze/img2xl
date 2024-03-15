# img2xl

### Description
This PyQt5-based app allows a user to choose a folder containing images with gps coordinates,
for example drone photos taken during automated mission flights.

"gui.py" is a file generated from Qt Designer, I have left it untouched at the moment.
"img2xl.py" contains functions that bind with gui elements (buttons, label). The app should be run from this file too.

After choosing the folder, click the 'Run' button to extract GPS data from images,
including lat-long coordinates and elevations.
Lat-long coordinates will be transformed into metric coordinates.

Then it will create an Excel file and put image names, coordinates and elevations in the file.

The folder "pictures" contains sample images and some other files to demonstrate data processing and exception handling.
Files and images with no GPS data shouldn't be processed.

The resulting Excel file will be placed in "output" folder

### Requirements
Python 3.x (recommended 3.9)
To install other required packages run in terminal: pip install -r requirements.txt
