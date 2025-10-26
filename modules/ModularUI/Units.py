import sys
import re
from PyQt6 import QtWidgets, QtCore, QtGui
from typing import Any, Callable, Dict, Optional, TypedDict, NotRequired
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
import modules.Misc as Misc
from modules.Misc import DirectoryManager


class Unit(TypedDict):
    """
    Типизированный словарь данных о юните.
    signalName: Имя сигнала к которому можно подключать методы
    dataType: Нативный тип данных юнита
    getData: Возвращает нативное значение из юнита
    setData: Устанавливает значение переданное в нативном типе
    clearData: Очищает или сбрасывает к стандартному значению данные в юните
    fromStrConverter: Извлекает данные из строки в нативный тип
    contextMenuActions: Список Actions в контекстном меню (Опциональный)
    defaultValue: Стандартное значение в юните (Опциональный)
    isCheckable: Является ли юнит отмечаемым (Опциональный)
    """

    signalName: str
    dataType: Any
    getData: Callable[[Any], Any]
    setData: Callable[[Any, Any], Any]
    clearData: Callable[[Any], Any]
    fromStrConverter: Callable[[str], Any]
    contextMenuActions: NotRequired[list[Misc.MenuUtils.MenuItem]]
    defaultValue: NotRequired[Any]
    isCheckable: NotRequired[bool]


# Словарь для преобразования в булевы значения
BOOL_MAP = dict.fromkeys({"Да", "Есть", "True", "1", "Yes", "Y"}, True)
BOOL_MAP.update(dict.fromkeys({"Нет", "False", "0", "No", "N"}, False))

# Вербальные названия юнитов
UNITS_NAMING = {
    "Строка": QtWidgets.QLineEdit,
    "Целое число": QtWidgets.QSpinBox,
    "Дробное число": QtWidgets.QDoubleSpinBox,
    "Дата и время": QtWidgets.QDateTimeEdit,
    "Флажок": QtWidgets.QCheckBox,
    "Картинка": QtWidgets.QLabel,
    "Ссылка на внешний файл данных": QtWidgets.QComboBox,
}

# Юниты
UNITS_MAP: Dict[Any, Unit] = {
    QtWidgets.QLineEdit: {
        "signalName": "textChanged",
        "dataType": str,
        "getData": lambda widget: widget.text(),
        "setData": lambda widget, data: widget.setText(data),
        "clearData": lambda widget: widget.clear(),
        "fromStrConverter": lambda data: str(data),
    },
    QtWidgets.QSpinBox: {
        "signalName": "valueChanged",
        "dataType": int,
        "getData": lambda widget: widget.value(),
        "setData": lambda widget, data: widget.setValue(data),
        "clearData": lambda widget: widget.setValue(widget.minimum()),
        "fromStrConverter": lambda data: int(re.sub("[^1234567890]", "", data)),
    },
    QtWidgets.QDoubleSpinBox: {
        "signalName": "valueChanged",
        "dataType": float,
        "getData": lambda widget: widget.value(),
        "setData": lambda widget, data: widget.setValue(data),
        "clearData": lambda widget: widget.setValue(widget.minimum()),
        "fromStrConverter": lambda data: float(re.sub("[^1234567890.]", "", data)),
    },
    QtWidgets.QCheckBox: {
        "signalName": "stateChanged",
        "dataType": bool,
        "getData": lambda widget: widget.isChecked(),
        "setData": lambda widget, data: widget.setChecked(data),
        "clearData": lambda widget: widget.setChecked(False),
        "fromStrConverter": lambda data: BOOL_MAP[data],
    },
    QtWidgets.QDateTimeEdit: {
        "signalName": "dateTimeChanged",
        "dataType": QtCore.QDateTime,
        "getData": lambda widget: widget.dateTime(),
        "setData": lambda widget, data: widget.setDateTime(data),
        "clearData": lambda widget: widget.setDateTime(
            QtCore.QDateTime.currentDateTime()
        ),
        "fromStrConverter": lambda data: QtCore.QDateTime.fromString(data),
    },
    QtWidgets.QLabel: {
        "signalName": "",
        "dataType": Misc.PickablePixmap,
        "getData": lambda widget: Misc.PickablePixmap(widget.pixmap()),
        "setData": lambda widget, data: widget.setPixmap(Misc.PickablePixmap(data)),
        "clearData": lambda widget: widget.setPixmap(Misc.PickablePixmap(None)),
        "fromStrConverter": lambda data: Misc.PickablePixmap(data),
    },
    QtWidgets.QComboBox: {
        "signalName": "",
        "dataType": str,
        "getData": lambda widget: widget.getCurrentText(),
        "setData": lambda widget, data: widget.setCurrentText(data),
        "clearData": lambda widget: widget.setCurrentIndex(0),
        "fromStrConverter": lambda data: str(data),
    },
}


class CustomCellWidget:
    """
    Сборщик виджета для QTableWidget.
    widget - Строка с вербальным названием виджета из списка UNITS_NAMING.
    """

    def __init__(self, widget: str):
        self.unit = UNITS_MAP.get(UNITS_NAMING[widget], UNITS_MAP[QtWidgets.QLineEdit])
        self._input_widget = UNITS_NAMING[widget]()  # or UNITS_NAMING["Строка"]()
        self._input_widget.setEnabled(False)
        self.data_type = self.unit["dataType"]
        self.setData = lambda data: self.unit["setData"](self._input_widget, data)
        if widget == "Картинка":
            self._input_widget.setFixedSize(300,300)


class CustomGroupBox(QtWidgets.QGroupBox):
    """
    Сборщик юнита.
    widget - Строка с вербальным названием виджета из списка UNITS_NAMING.
    parent - Родительский виджет (Опционально)
    """

    def __init__(self, widget: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.unit = UNITS_MAP.get(UNITS_NAMING[widget], UNITS_MAP[QtWidgets.QLineEdit])
        self._input_widget = UNITS_NAMING[widget](self) or UNITS_NAMING["Строка"](self)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().addWidget(self._input_widget)
        self.signal_name = self.unit["signalName"]
        self.data_type = self.unit["dataType"]
        self.setData = lambda data: self.unit["setData"](self._input_widget, data)
        self.getData = lambda: self.unit["getData"](self._input_widget)
        self.clearData = self.unit["clearData"]
        if "contextMenuActions" in self.unit:
            self.context_menu = QtWidgets.QMenu(self)
            prepareContextMenu(self.context_menu, self.unit["contextMenuActions"])
            self._input_widget.setContextMenuPolicy(
                QtCore.Qt.ContextMenuPolicy.CustomContextMenu
            )
            self._input_widget.customContextMenuRequested.connect(self.addContextMenu)
        if "isCheckable" in self.unit:
            self.setCheckable(self.unit["isCheckable"])

    def connectMethod(self, method: Callable[[Any], None]) -> None:
        getattr(self._input_widget, self.signal_name).connect(method)

    def addContextMenu(self, pos: QtCore.QPoint) -> None:
        self.context_menu.exec(self._input_widget.mapToGlobal(pos))


class PixmapGroupBox(QtWidgets.QGroupBox):
    def __init__(self, parent: Optional[QtWidgets.QWidget]):
        super().__init__(parent)
        self.unit = QtWidgets.QLabel(self)
        self.changeButton = QtWidgets.QPushButton("Выбрать картинку",self)
        self.changeButton.clicked.connect(self.changePixmap)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().addWidget(self.unit)
        self.layout().addWidget(self.changeButton)
        self.setData = lambda data: self.unit.setPixmap(Misc.PickablePixmap(data))
        self.getData = lambda: Misc.PickablePixmap(self.unit.pixmap())
        self.clearData = lambda: self.unit.setPixmap(Misc.PickablePixmap(None))
        self.connectedMethod = None
    def changePixmap(self) -> None:
        filename, ok = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберете картинку", str(Path.home()), "Images (*.png *.jpg)"
        )
        path = Path(filename)
        self.setData(str(path)) if filename else self.clearData()
        try:
            self.connectedMethod() if self.connectedMethod is not None else None
        except:
            pass

    def connectMethod(self, method: Callable[[Any], None]) -> None:
        self.connectedMethod = method


class DataComboBox(QtWidgets.QGroupBox):
    def __init__(self, path: str, parent: Optional[QtWidgets.QWidget]):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.unit = QtWidgets.QComboBox(self)
        self.data_view = QtWidgets.QTableWidget(self)
        self.layout().addWidget(self.data_view)
        self.layout().addWidget(self.unit)
        self.setData = lambda data: self.unit.setCurrentText(Path(data).name)
        self.getData = lambda: self.unit.currentText()
        self.DirManager = DirectoryManager.DirectoryManager(path)
        self.view_widgets = []
        for i in range(len(self.DirManager.directory_data)):
            self.unit.addItem(
                str(Path(self.DirManager.paths_list[i]).name),
                userData=self.DirManager.paths_list[i],
            )
        self.data_view.setRowCount(len(self.DirManager.config_file))
        self.data_view.setColumnCount(1)
        for i in range(len(self.DirManager.config_file)):
            self.data_view.setVerticalHeaderItem(
                i,
                QtWidgets.QTableWidgetItem(self.DirManager.config_file[i]["header"]),
            )
            cellWidget = CustomCellWidget(self.DirManager.config_file[i]["unit"])
            self.view_widgets.append(cellWidget)
            self.data_view.setCellWidget(i, 0, cellWidget._input_widget)
            self.data_view.resizeColumnsToContents()
            self.data_view.resizeRowsToContents()
        self.connectMethod(self.updateDataView)
    def updateDataView(self):
        for i in range(len(self.view_widgets)):
            self.view_widgets[i].setData(
                self.DirManager.directory_data[self.unit.currentText()][i]
            )

    def connectMethod(self, method):
        self.unit.activated.connect(method)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    for widget in UNITS_NAMING:
        group_box = CustomGroupBox(widget)
        group_box.setTitle(f"Test {widget}")

        def on_change(value: Any) -> None:
            print(f"{widget} changed: {value}")

        group_box.connectMethod(on_change)
        layout.addWidget(group_box)
    window.show()
    sys.exit(app.exec())
