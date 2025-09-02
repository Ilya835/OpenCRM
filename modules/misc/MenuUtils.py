from PyQt6 import QtWidgets, QtGui
from typing import Any, Dict, List, Union, Optional, NotRequired, TypedDict

module_name = "Дополнительные утилиты для QMenuBar"


class MenuItem(QtGui.QAction):
    def __init__(
        self, title: str, method: Any, checkable: bool, icon: QtGui.QIcon, objName: str
    ):
        super().__init__()
        self.setText(title)
        self.triggered.connect(method)
        self.setCheckable(checkable)
        self.setIcon(icon)
        self.setObjectName(objName)


def setupMenuBar(
    menubar: QtWidgets.QMenuBar,
    content: Dict[str, List[Union[MenuItem, None]]],
    parent: QtWidgets.QGroupBox,
) -> None:
    for i in list(content.keys()):
        menu = QtWidgets.QMenu(i, menubar)
        for j in content[i]:
            if j is None:
                menu.addSeparator()
            else:
                j.setParent(menu)
                menu.addAction(j)
        menubar.addMenu(menu)
        menu.show()
    parent.layout().setMenuBar(menubar)


class ContextMenuAction(TypedDict):
    text: str
    method: Any
    icon: NotRequired[QtGui.QIcon]


def createQAction(
    menu_action: ContextMenuAction, parent: Optional[QtWidgets.QWidget]
) -> QtGui.QAction:
    action = QtGui.QAction()
    action.setText(menu_action["text"])
    action.triggered.connect(menu_action["method"])
    if parent:
        action.setParent(parent)
    action.setIcon(menu_action.get("icon", QtGui.QIcon(None)))
    return action


def prepareContextMenu(
    context_menu: QtWidgets.QMenu, content: list[ContextMenuAction]
) -> None:
    for action in content:
        context_menu.addAction(createQAction(action, context_menu))
