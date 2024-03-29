import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
import time
import openpyxl as xl
import exifread
import pathlib
import pyproj


def decimal_coord(coordinate):
    """Processes single coordinate (latitude or longitude) into decimal degrees format"""
    coord_list = coordinate.lstrip('[').rstrip(']').split(', ')
    coord_deg = int(coord_list[0])
    coord_min = int(coord_list[1])
    coord_sec = int(coord_list[2].split('/')[0]) / int(coord_list[2].split('/')[1])
    dec_coord = (coord_sec / 60 + coord_min) / 60 + coord_deg

    return dec_coord


def data_extractor(file):
    """Extracts data from a single file"""
    if file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.tiff'):
        try:
            tags = exifread.process_file(open(file, 'rb'))
            geo = {i: tags[i] for i in tags.keys() if i.startswith('GPS')}

            lat = str(geo['GPS GPSLatitude'])
            lon = str(geo['GPS GPSLongitude'])
            dec_lat, dec_lon = decimal_coord(lat), decimal_coord(lon)

            # Extract altitude from an image
            alt = str(geo['GPS GPSAltitude'])
            alt_list = alt.split('/')
            altitude = int(alt_list[0]) / int(alt_list[1])

            # Lat/Long to metric conversion
            pp = pyproj.Proj(proj='utm', zone=38, ellps='WGS84', preserve_units=False)
            x, y = pp(dec_lon, dec_lat)

            # Return a tuple representing each Excel row
            return file.stem, x, y, altitude
        except:  # No need to catch any specific error
            return None
    else:
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the user interface from Designer
        self.ui = loadUi("ui/gui.ui", self)

        # Initializing path as any string
        self.path = "Empty path"

        # Link pushButtons with corresponding functions
        self.ui.pushButton.clicked.connect(self.get_folder)
        self.ui.pushButton_2.clicked.connect(self.write_excel)

    def get_folder(self):
        """Opens a file dialog to choose a directory. 
        This method is linked with pushbutton"""
        path = QFileDialog.getExistingDirectory()

        if path:  # Update the label and initial variable if the directory is chosen
            self.path = path
            self.ui.label.setText(f"Selected Directory: {self.path}")
        else:  # If no directory was selected do nothing
            pass

    def extract_gps_data(self):
        """Extracts GPS data from images"""

        target_folder = pathlib.Path(self.path)

        geodata_rows = []  # A list of Excel rows
        files_list = list(target_folder.iterdir())  # List of files in selected folder

        for file in files_list:
            row = data_extractor(file)
            if row:
                geodata_rows.append(row)

        return geodata_rows

    def write_excel(self):
        """Calls extract_gps_data() method, then writes extracted data to Excel.
        This method is linked with pushbutton_2"""

        if not pathlib.Path(self.path).is_dir():
            QMessageBox.warning(None, 'No folder selected', 'Select a folder first and try again')
        elif len(self.extract_gps_data()) > 0:
            # Initialize Excel workbook and sheet
            wb = xl.Workbook()
            sheet = wb.active

            # Iterate over rows list and insert them in Excel
            start_time = time.perf_counter()
            for row in self.extract_gps_data():
                sheet.append(row)
            end_time = time.perf_counter()
            try:
                wb.save('output/Image_coordinates.xlsx')
                self.ui.label_2.setStyleSheet("background-color:transparent; color:rgb(0, 170, 127)")
                self.ui.label_2.setText("Success")
                self.ui.label_3.setStyleSheet("background-color:transparent")
                self.ui.label_3.setText(f"Finished in {round(end_time - start_time, 2)}")
            except PermissionError:
                QMessageBox.critical(None, 'File is open', 'Please close excel file and try again')
        else:
            QMessageBox.critical(None, 'No GPS Data Found', 'Folder contains no images or images have no coordinates')
