#!/usr/bin/env python3
from PyQt6 import QtWidgets
from modules.Misc import DirectoryManager
from modules import ui_files
from modules.ModularUI.Areas import DirectoryExplorer, FileEditor



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = ui_files.TestWindow.Ui_Window()
        self.ui.setupUi(self)
        self.DirManager = DirectoryManager.DirectoryManager(
            "/home/ilya/Projects/OpenCRM/test/dir1/"
        )  # Экземпляр класса DirectoryManager для работы с фалами в папке (чтение, запись и т.д).
        self.enters = (
            FileEditor(self.DirManager)
        )  # Экземпляр класса FileEditor содержащий в себе поля ввода.
        self.explorer = DirectoryExplorer(
            self.DirManager
        )  # Экземпляр класса DirectoryExplorer - таблицы с файлами и их контентом являющейся селектором файлов.
        self.enters.selector = self.explorer
        # self.explorer.enters = self.enters
        self.ui.splitter.addWidget(self.enters)
        self.ui.splitter_2.addWidget(self.explorer)
        self.explorer.update()
        # self.enters.update()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
