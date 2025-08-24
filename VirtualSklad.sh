#!/usr/bin/env python3
import sys
from PyQt6 import QtWidgets
from modules import inputs, widgets, misc
import ui_files


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui_files.VirtualSklad.Ui_Window()
        self.ui.setupUi(self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
