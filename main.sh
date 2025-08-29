#!/usr/bin/env python3
import logging
from PyQt6 import QtWidgets
from modules.areas import Areas
from modules.misc import Misc
from modules import ui_files

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
        self.directoryWorker = Misc[
            "Менеджер папки"
        ](
            "/home/ilya/Projects/OpenCRM/test/dir1/"
        )  # Экземпляр класса DirectoryWorker для работы с фалами в папке (чтение, запись и т.д).
        self.enters = Areas["Редактор файла"](
            self.directoryWorker
        )  # Экземпляр класса FileEnters содержащий в себе поля ввода.
        self.explorer = Areas[
            "Обзор папки"
        ](
            self.directoryWorker
        )  # Экземпляр класса DirectoryExplorer - таблицы с файлами и их контентом являющейся селектором файлов.
        self.enters.selector = self.explorer
        self.explorer.enters = self.enters
        self.ui.splitter.addWidget(self.enters)
        self.ui.splitter_2.addWidget(self.explorer)
        self.explorer.update()
        self.enters.update()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
