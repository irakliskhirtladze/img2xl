# img2xl

This PyQt5-based app allows an user to choose a folder containing images with gps coordinates, for example drone photos taken during automated mission flights.

"gui.py" is a file generated from Qt Designer, I have left it untouched at the moment.
"img2xl.py" contains functions that bind with gui elements (buttons, label). The app should be run from this file too.

After choosing the folder, clicking the 'Run' button will extract GPS data from images, including lat-long coordinates and elevations. Lat-long coordinates will be transformed into metric coordinates.

Then it will create an Excel file and put image names, coordinates and elevations in the file.

The folder "pictures" contains sample images and some other files to demonstrate data processing and exception handling. Files and images with no GPS data shouldn't be processed.