from PyQt6 import QtWidgets, QtCore
from ..misc import MenuUtils, DirectoryManager

from ..icons import Icons
from typing import Any, Dict, Union, List

module_name = "Редактор заголовочного файла"


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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    layout.addWidget(HeaderEditor())
    window.show()
    sys.exit(app.exec())
