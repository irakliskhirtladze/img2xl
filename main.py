import sys
from modules.img2xl import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("IMG2XL")
    window.setWindowIcon(QIcon("assets/uav.ico"))
    window.show()
    sys.exit(app.exec_())
