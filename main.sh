#!/usr/bin/env python3
import logging
from PyQt6 import QtWidgets
from modules import misc, widgets
import ui_files

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"./logs/{__name__}.log", mode="w")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui_files.TestWindow.Ui_Window()
        self.ui.setupUi(self)
        self.directoryWorker = misc.content[
            "Менеджер папки"
        ](
            "/home/ilya/Projects/OpenCRM/"
        )  # Экземпляр класса DirectoryWorker для работы с фалами в папке (чтение, запись и т.д).
        self.enters = widgets.content["Редактор файла"](
            self.directoryWorker
        )  # Экземпляр класса FileEnters содержащий в себе поля ввода.
        self.explorer = widgets.content[
            "Обзор папки"
        ](
            self.directoryWorker
        )  # Экземпляр класса DirectoryExplorer - таблицы с файлами и их контентом являющейся селектором файлов.
        self.enters.selector = self.explorer
        self.explorer.enters = self.enters
        self.ui.splitter.addWidget(self.enters)
        self.ui.splitter_2.addWidget(self.explorer)

        def filteringSwitch():
            self.explorer.filtering = self.ui.is_filter.isChecked()
            self.explorer.update()

        self.ui.is_filter.triggered.connect(filteringSwitch)
        self.enters.update()
        self.explorer.update()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
