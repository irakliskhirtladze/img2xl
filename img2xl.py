import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from gui import Ui_MainWindow
import openpyxl as xl
import exifread
import pathlib
import pyproj

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)    
        
        # Links pushbuttons with corresponding functions
        self.ui.pushButton.clicked.connect(self.getfolder)
        self.ui.pushButton_2.clicked.connect(self.write_excel)

    def getfolder(self):
        """Opens a file dialog to choose a directory. 
        This method is linked with pushbutton"""
        self.path = QFileDialog.getExistingDirectory()
        
        if self.path:
            # Update the label if the directory is chosen
            self.ui.label.setText(f"Selected Directory: {self.path}")
        else:
            # If no directory was selected do nothing
            pass      

    def extract_gps_data(self):
        """Extracts GPS data from images"""

        target_folder = pathlib.Path(self.path)

        geodata_rows = [] # A list which will be filled with Excel rows
        self.files_list=list(target_folder.iterdir()) # Get a list of files present in selected folder
        self.counter = 0 # This counts how many files were processed successfully

        for file in self.files_list:
            if file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.tiff'):
                try: # Try to process all image files
                    tags = exifread.process_file(open(file, 'rb'))
                    geo={i:tags[i] for i in tags.keys() if i.startswith('GPS')}
                  
                    # Get degree, minute, second for latitude and convert them to decimal degrees
                    lat = str(geo['GPS GPSLatitude'])
                    latlist = lat.lstrip('[').rstrip(']').split(', ')
                    latdeg = int(latlist[0])
                    latmin = int(latlist[1])
                    latsec = int(latlist[2].split('/')[0])/int(latlist[2].split('/')[1])
                    declat=(latsec/60+latmin)/60+latdeg
                    
                    # Get degree, minute, second for longitude and convert them to decimal degrees
                    lon = str(geo['GPS GPSLongitude'])
                    lonlist = lon.lstrip('[').rstrip(']').split(', ')
                    londeg = int(lonlist[0])
                    lonmin = int(lonlist[1])
                    lonsec = int(lonlist[2].split('/')[0])/int(lonlist[2].split('/')[1])
                    declon = (lonsec/60+lonmin)/60+londeg
                    
                    # Extract altitude from an image
                    alt = str(geo['GPS GPSAltitude'])
                    altlist = alt.split('/')
                    altitude = int(altlist[0])/int(altlist[1])
                    
                    # Lat/Long to X/Y conversion
                    pp = pyproj.Proj(proj='utm', zone=38, ellps='WGS84', preserve_units=False)
                    X, Y = pp(declon, declat)

                    # Make a tuple representing each Excel row and add to list
                    row = (file.stem, X, Y, altitude)
                    geodata_rows.append(row)

                    self.counter += 1

                except: # Move on to the next file if it fails
                    continue   

        return geodata_rows
    
    def write_excel(self):
        """Calls extract_gps_data() method, then writes extracted data to Excel.
        This method is linked with pushbutton_2"""

        if not pathlib.Path(self.path).is_dir():
            QMessageBox.warning(None, 'No folder selected', 'Select a folder first and try again')
        elif len(self.extract_gps_data())>0:
            # Initialize Excel workbook and sheet
            wb = xl.Workbook()
            sheet = wb.active

            # Iterate over rows list and insert them into the Excel sheet
            for row in self.extract_gps_data():
                sheet.append(row)
            try:
                wb.save(self.path + '/Image_coordinates.xlsx')
                QMessageBox.information(None, 'Success!', f'{self.counter} out of {len(self.files_list)} files were processed')
            except PermissionError:
                QMessageBox.critical(None, 'Open File', 'Please close excel file and try again')
        else:
            QMessageBox.critical(None,'No GPS Data Found', 'Folder contains no images or images have no cooridnates')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())