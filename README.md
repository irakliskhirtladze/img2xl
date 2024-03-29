# img2xl

## Description
This PyQt5-based app allows a user to choose a folder containing images with gps coordinates,
for example drone photos taken during automated mission flights.

- Run 'main.py' to start using the app.
- "ui/gui.ui" is a file generated from Qt Designer.
- "modules/img2xl.py" contains functions that bind with GUI elements (buttons, label).
- Choose a folder with images and click the 'Run' button to extract GPS data from images,
including lat-long coordinates and elevations.
- Lat-long coordinates will be transformed into metric coordinates.
Then it will create an Excel file and put image names, coordinates and elevations in the file.

The resulting Excel file will be placed in "output" folder

## Requirements
- Python 3.x (recommended 3.9)

To install other required packages run in terminal:
````
pip install -r requirements.txt
