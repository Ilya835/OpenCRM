from PyQt6 import QtGui, QtWidgets
from typing import List, Dict, Union, Callable, Any
class MenuUtils:
    """
    Набор утилит для работы с QMenuBar и QMenu.
    """

    class MenuItem(QtGui.QAction):
        def __init__(
            self,
            title: str,
            method: Callable[[Any], Any],
            checkable: bool = False,
            icon: Union[QtGui.QIcon, None] = None,
            objName: Union[str, None] = None,
        ):
            """
            Создает объект типа QAction из переданных при инициализации переменных.
            """
            super().__init__()
            self.setText(title)
            self.triggered.connect(method)
            self.setCheckable(checkable)
            if icon is not None:
                self.setIcon(icon)
            if objName is not None:
                self.setObjectName(objName)

    def setupMenuBar(
        self,
        menubar: QtWidgets.QMenuBar,
        content: Dict[str, List[Union[MenuItem, None]]],
        parent: QtWidgets.QGroupBox,
    ) -> None:
        """
        Создает ManuBar у переданного parent.
        """
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

    def setupContextMenu(
        self, context_menu: QtWidgets.QMenu, content: List[Union[MenuItem, None]]
    ) -> None:
        for action in content:
            if action is not None:
                context_menu.addAction(action)
            else:
                context_menu.addSeparator()

MainClass = MenuUtils
