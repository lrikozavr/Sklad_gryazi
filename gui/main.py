import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from add_window import WidgetGallery
if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    availableGeometry = mainWindow.screen().availableGeometry()
    mainWindow.resize(availableGeometry.width(), availableGeometry.height())
    mainWindow.show()

    #mainWindow.open()
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())