from PyQt6 import QtWidgets, QtCore
from typing import Any, Callable, Dict, Optional, TypedDict, NotRequired
from .misc import MenuUtils
import re


class Unit(TypedDict):
    signalName: str
    dataType: Any
    getData: Callable[[Any], Any]
    setData: Callable[[Any, Any], Any]
    clearData: Callable[[Any], Any]
    fromStrConverter: Callable[[str], Any]
    contextMenuActions: NotRequired[list[MenuUtils.ContextMenuAction]]
    defaultValue: NotRequired[Any]
    isCheckable: NotRequired[bool]


TYPES_MAPPING = {
    "Строка": QtWidgets.QLineEdit,
    "Целое число": QtWidgets.QSpinBox,
    "Дробное число": QtWidgets.QDoubleSpinBox,
    "Дата и время": QtWidgets.QDateTimeEdit,
    "Флажок": QtWidgets.QCheckBox,
}
BOOL_MAP = dict.fromkeys({"Да", "Есть", "True", "1", "Yes", "Y"}, True)
BOOL_MAP.update(dict.fromkeys({"Нет", "False", "0", "No", "N"}, False))

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
        "signalName": "datetimeChanged",
        "dataType": QtCore.QDateTime,
        "getData": lambda widget: widget.isChecked(),
        "setData": lambda widget, data: widget.setDateTime(data),
        "clearData": lambda widget: widget.setDateTime(
            QtCore.QDateTime.currentDateTime()
        ),
        "fromStrConverter": lambda data: QtCore.QDateTime.fromString(data),
    },
}


class CustomGroupBox(QtWidgets.QGroupBox):
    def __init__(self, widget: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.unit = UNITS_MAP.get(TYPES_MAPPING[widget], UNITS_MAP[QtWidgets.QLineEdit])
        self._input_widget = TYPES_MAPPING[widget](self) or TYPES_MAPPING["Строка"](
            self
        )
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(6, 12, 6, 6)
        self.layout().addWidget(self._input_widget)
        self.signal_name = self.unit["signalName"]
        self.data_type = self.unit["dataType"]
        self.setData = lambda data: self.unit["setData"](self._input_widget, data)
        self.getData = lambda: self.unit["getData"](self._input_widget)
        self.clearData = self.unit["clearData"]
        if "contextMenuActions" in self.unit:
            self.context_menu = QtWidgets.QMenu(self)
            MenuUtils.prepareContextMenu(
                self.context_menu, self.unit["contextMenuActions"]
            )
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


# Пример использования
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(window)
    for widget in TYPES_MAPPING:
        group_box = CustomGroupBox(widget)
        group_box.setTitle(f"Test {widget}")

        def on_change(value):
            print(f"{widget} changed: {value}")

        group_box.connectMethod(on_change)
        layout.addWidget(group_box)
    window.show()
    sys.exit(app.exec())
