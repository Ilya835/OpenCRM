from PyQt6 import QtWidgets, QtGui
from typing import Any, Dict

module_name = "Дополнительные утилиты для QMenuBar"


def setupMenuBar(
    menubar: QtWidgets.QMenuBar,
    content: Dict[str, Dict[str, Dict[str, Any]]],
    parent: QtWidgets.QGroupBox,
) -> None:
    for i in list(content.keys()):
        menu = QtWidgets.QMenu(i, menubar)
        for j in list(content[i].keys()):
            if j == "separator":
                menu.addSeparator()
            else:
                action = QtGui.QAction(j, menu)
                action.triggered.connect(content[i][j]["onTriggered"])
                action.setCheckable(content[i][j]["checkable"])
                action.setIcon(content[i][j]["icon"])
                action.setObjectName(content[i][j]["objName"])
                menu.addAction(action)
        menubar.addMenu(menu)
        menu.show()
    parent.layout().setMenuBar(menubar)
