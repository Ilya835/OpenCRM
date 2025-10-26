import sys
from PyQt6 import QtGui, QtCore, QtWidgets
from typing import Any
from pathlib import Path

inProjectRoot: bool = False
projectRoot: str = str(Path(__file__).resolve())
upToFolders: int = 0
while not inProjectRoot:
    projectRoot = str(Path(__file__).resolve().parents[upToFolders])
    if projectRoot.endswith("OpenCRM"):
        inProjectRoot = True
    upToFolders += 1
sys.path.append(projectRoot)

from modules.Misc import MenuUtils, DirectoryManager
from content.icons import Icons
from modules.ModularUI.Areas import FileEditor
from modules.ModularUI.Units import UNITS_MAP, UNITS_NAMING, CustomCellWidget


class DirectoryExplorer(QtWidgets.QGroupBox):
    def __init__(self, DirManager: DirectoryManager):
        super().__init__()
        self.DirManager = DirManager
        self.table = QtWidgets.QTableWidget(self)
        self.update_data()
        self.setLayout(QtWidgets.QGridLayout(self))
        self.layout().addWidget(self.table)
        menubar_content: Dict[str, List[Union[MenuBarUtils.MenuItem, None]]] = {
            "Файл": [],
            "Изменить": [],
        }
        self.menubar = QtWidgets.QMenuBar(self)
        MenuUtils.setupMenuBar(MenuUtils, self.menubar, menubar_content, self)

    def update_data(self):
        self.table.clear()
        self.table.setColumnCount(len(self.DirManager.config_file))
        self.table.setRowCount(len(self.DirManager.directory_data))
        for i in range(len(self.DirManager.config_file)):
            self.table.setHorizontalHeaderItem(
                i, QtWidgets.QTableWidgetItem(self.DirManager.config_file[i]["header"])
            )
        for i in range(len(self.DirManager.directory_data.values())):
            self.table.setVerticalHeaderItem(
                i,
                QtWidgets.QTableWidgetItem(
                    list(self.DirManager.directory_data.keys())[i]
                ),
            )
            for j in range(len(self.DirManager.config_file)):
                widget = CustomCellWidget(self.DirManager.config_file[j]["unit"])
                widget.setData(list(self.DirManager.directory_data.values())[i][j])
                self.table.setCellWidget(i, j, widget._input_widget)


MainClass = DirectoryExplorer
