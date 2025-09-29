from PyQt6 import QtWidgets
import sys
from pathlib import Path
from typing import Any, Dict, Union, List, Optional

inProjectRoot: bool = False
projectRoot: str = str(Path(__file__).resolve())
upToFolders: int = 0
while not inProjectRoot:
    projectRoot = str(Path(__file__).resolve().parents[upToFolders])
    if projectRoot.endswith("OpenCRM"):
        inProjectRoot = True
    upToFolders += 1
sys.path.append(projectRoot)

from modules.Units import UNITS_NAMING
from modules.icons import Icons
from modules.Misc.DirectoryManager import DirectoryManager


class TypesEditor(QtWidgets.QGroupBox):
    def __init__(self, DirManager: Union[DirectoryManager, None]) -> None:
        super().__init__()

        layout = QtWidgets.QGridLayout(self)

        def addField() -> None:
            field = QtWidgets.QComboBox(self)
            for unit in UNITS_NAMING:
                field.addItem(unit, UNITS_NAMING[unit])
            layout.addWidget(field, layout.rowCount(), 0)
            deleteButton = QtWidgets.QPushButton("Удалить тип", self)
            deleteButton.clicked.connect(field.deleteLater)
            deleteButton.clicked.connect(deleteButton.deleteLater)
            layout.addWidget(deleteButton, layout.rowCount() - 1, 1)

        addButton = QtWidgets.QPushButton("Добавить тип", self)
        addButton.clicked.connect(addField)
        layout.addWidget(addButton)
MainClass = TypesEditor

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    layout.addWidget(TypesEditor())
    window.show()
    sys.exit(app.exec())
