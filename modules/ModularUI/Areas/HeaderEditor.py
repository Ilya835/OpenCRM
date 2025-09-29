import sys
from PyQt6 import QtWidgets
from typing import Any, Dict, Union, List
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
from modules.icons import Icons

class HeaderEditor(QtWidgets.QGroupBox):
    def __init__(self, DirManager: DirectoryManager) -> None:
        super().__init__()

        layout = QtWidgets.QGridLayout(self)

        def addField() -> None:
            field = QtWidgets.QLineEdit(self)
            layout.addWidget(field, layout.rowCount(), 0)
            deleteButton = QtWidgets.QPushButton("Удалить заголовок", self)
            deleteButton.clicked.connect(field.deleteLater)
            deleteButton.clicked.connect(deleteButton.deleteLater)
            layout.addWidget(deleteButton, layout.rowCount() - 1, 1)

        addButton = QtWidgets.QPushButton("Добавить заголовок", self)
        addButton.clicked.connect(addField)
        layout.addWidget(addButton)
MainClass = HeaderEditor

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    layout.addWidget(HeaderEditor())
    window.show()
    sys.exit(app.exec())
