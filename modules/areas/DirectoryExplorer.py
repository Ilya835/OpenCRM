from ..misc import MenuBarUtils
from ..icons import Icons
from PyQt6 import QtGui, QtCore, QtWidgets
from typing import Any

module_name = "Обзор папки"


class DirectoryExplorer(QtWidgets.QGroupBox):
    def __init__(self, directoryWorker: Any):
        def nullDef() -> None:
            pass

        super().__init__()
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(DirectoryTable(directoryWorker))
        menubar_content: Dict[str, Dict[str, Dict[str, Any]]] = {
            "Файл": {
                "Открыть": {
                    "onTriggered": nullDef,
                    "checkable": False,
                    "icon": Icons["open-file.svg"],
                    "objName": "open",
                },
                "separator": None,
                "Сохранить": {
                    "onTriggered": nullDef,
                    "checkable": False,
                    "icon": Icons["save-file.svg"],
                    "objName": "save",
                },
                "Удалить": {
                    "onTriggered": nullDef,
                    "checkable": False,
                    "icon": Icons["trashbox.svg"],
                    "objName": "detele",
                },
            },
            "Изменить": {
                "Отфильтровать данные": {
                    "onTriggered": nullDef,
                    "checkable": True,
                    "icon": Icons["filter-files.svg"],
                    "objName": "filter",
                }
            },
        }
        self.menubar = QtWidgets.QMenuBar(self)
        MenuBarUtils.setupMenuBar(self.menubar, menubar_content, self)
        self.setLayout(layout)


class DirectoryTable(QtWidgets.QTableView):
    def __init__(self, directoryWorker: Any):
        super().__init__()
        self.directoryWorker = directoryWorker
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
        model = DictArrayTableModel(self.directoryWorker)
        self.setModel(model)


class DictArrayTableModel(QtCore.QAbstractTableModel):
    def __init__(self, directoryWorker: Any):
        super().__init__()
        self.directoryWorker = directoryWorker

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.directoryWorker.data_files)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if not self.directoryWorker.data_files:
            return 0
        return len(next(iter(self.directoryWorker.data_files.values())))

    def data(
        self, index: QtCore.QModelIndex, role: Any = QtCore.Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if not index.isValid():
            return None
        col = index.column()
        value = self.directoryWorker.data_files[
            list(self.directoryWorker.data_files.keys())[index.row()]
        ][col]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if self.directoryWorker.config_files["TYPES"][col] == "Фото":
                return None
            elif self.directoryWorker.config_files["TYPES"][col] == "Время":
                return value.toString(self.directoryWorker.config_files["FORMAT"][col])
            elif self.directoryWorker.config_files["TYPES"][col] == "Флажок":
                return "Да" if value else "Нет"
            else:
                return str(value)

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            if self.directoryWorker.config_files["TYPES"][col] == "Фото":
                return QtGui.QIcon(value)
            return None

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if self.directoryWorker.config_files["TYPES"][col] in [
                "Целое число",
                "Дробное число",
            ]:
                return (
                    QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            elif self.directoryWorker.config_files["TYPES"][col] == "Время":
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
                if section < len(self.directoryWorker.config_files["HEADER"]):
                    return self.directoryWorker.config_files["HEADER"][section]
            elif orientation == QtCore.Qt.Orientation.Vertical:
                if section < len(self.directoryWorker.data_files.keys()):
                    return list(self.directoryWorker.data_files.keys())[section]
        return None

    def flags(
        self, index: QtCore.QModelIndex
    ) -> QtCore.Qt.ItemFlag | QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
