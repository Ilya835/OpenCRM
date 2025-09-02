from ..misc import MenuUtils, DirectoryManager
from ..icons import Icons
from . import FileEditor
from PyQt6 import QtGui, QtCore, QtWidgets
from typing import Any, Dict

module_name = "Обзор папки"


class DirectoryExplorer(QtWidgets.QGroupBox):
    def __init__(self, DirManager: DirectoryManager):
        def nullDef() -> None:
            pass

        super().__init__()
        self.setLayout(QtWidgets.QGridLayout(self))
        self.layout().addWidget(DirectoryTable(DirManager))
        # menubar_content: Dict[str, List[Union[MenuBarUtils.MenuItem, None]]] = {
        #    "Файл": [],
        #    "Изменить": [],
        # }
        self.menubar = QtWidgets.QMenuBar(self)
        # MenuBarUtils.setupMenuBar(self.menubar, menubar_content, self)


class DirectoryTable(QtWidgets.QTableView):
    def __init__(self, DirManager: DirectoryManager):
        super().__init__()
        self.DirManager = DirManager
        self.setup_ui()
        self.set_data()
        self.setIconSize(QtCore.QSize(128, 128))

    def setup_ui(self) -> None:
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

    def set_data(self) -> None:
        model = DictArrayTableModel(self.DirManager)
        self.setModel(model)


class DictArrayTableModel(QtCore.QAbstractTableModel):
    def __init__(self, DirManager: DirectoryManager):
        super().__init__()
        self.DirManager = DirManager

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.DirManager.raw_data_files)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if not self.DirManager.data_files:
            return 0
        return len(next(iter(self.DirManager.raw_data_files.values())))

    def data(
        self, index: QtCore.QModelIndex, role: Any = QtCore.Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if not index.isValid():
            return None
        col = index.column()
        value = self.DirManager.raw_data_files[
            list(self.DirManager.raw_data_files.keys())[index.row()]
        ][col]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if self.DirManager.config_files["TYPES"][col] == "Фото":
                return None
            elif self.DirManager.config_files["TYPES"][col] == "Время":
                return value.toString(self.DirManager.config_files["FORMAT"][col])
            elif self.DirManager.config_files["TYPES"][col] == "Флажок":
                return "Да" if value else "Нет"
            else:
                return str(value)

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            if self.DirManager.config_files["TYPES"][col] == "Фото":
                return QtGui.QIcon(value)
            return None

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if self.DirManager.config_files["TYPES"][col] in [
                "Целое число",
                "Дробное число",
            ]:
                return (
                    QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            elif self.DirManager.config_files["TYPES"][col] == "Время":
                return (
                    QtCore.Qt.AlignmentFlag.AlignCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            return (
                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
            )

        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return value

        return None

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: Any = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                if section < len(self.DirManager.config_files["HEADER"]):
                    return self.DirManager.config_files["HEADER"][section]
            elif orientation == QtCore.Qt.Orientation.Vertical:
                if section < len(self.DirManager.data_files.keys()):
                    return list(self.DirManager.data_files.keys())[section]
        return None

    def flags(
        self, index: QtCore.QModelIndex
    ) -> QtCore.Qt.ItemFlag | QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
