#!/usr/bin/env python3
import logging
from PyQt6 import QtWidgets
from modules.misc.DirectoryManager import DirectoryManager
from modules import ui_files
from modules.areas.DirectoryExplorer import DirectoryExplorer
from modules.areas.FileEditor import FileEditor
from modules.areas.HeaderEditor import HeaderEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"./logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = ui_files.TestWindow.Ui_Window()
        self.ui.setupUi(self)
        self.DirManager = DirectoryManager(
            "/home/ilya/Projects/OpenCRM/test/dir1/"
        )  # Экземпляр класса DirectoryManager для работы с фалами в папке (чтение, запись и т.д).
        self.enters = (
            HeaderEditor()
        )  # Экземпляр класса FileEditor содержащий в себе поля ввода.
        self.explorer = DirectoryExplorer(
            self.DirManager
        )  # Экземпляр класса DirectoryExplorer - таблицы с файлами и их контентом являющейся селектором файлов.
        # self.enters.selector = self.explorer
        # self.explorer.enters = self.enters
        self.ui.splitter.addWidget(self.enters)
        self.ui.splitter_2.addWidget(self.explorer)
        self.explorer.update()
        # self.enters.update()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
