from ..units import Units
from ..icons import Icons
from ..misc import MenuBarUtils
from PyQt6 import QtWidgets, QtGui
from typing import Any, Dict

module_name = "Редактор файла"


class FileEditor(QtWidgets.QGroupBox):
    def __init__(self, directoryWorker):
        super(FileEditor, self).__init__()
        self.directoryWorker = directoryWorker  # Объект менеджера папок
        menubar_content: Dict[str, Dict[str, Dict[str, Any]]] = {
            "Файл": {
                "Открыть": {
                    "onTriggered": self.openFile,
                    "checkable": False,
                    "icon": Icons["open-file.svg"],
                    "objName": "open",
                },
                "separator": None,
                "Сохранить": {
                    "onTriggered": self.showSaveFileDialog,
                    "checkable": False,
                    "icon": Icons["save-file.svg"],
                    "objName": "save",
                },
                "Удалить": {
                    "onTriggered": self.deleteFile,
                    "checkable": False,
                    "icon": Icons["trashbox.svg"],
                    "objName": "detele",
                },
            },
            "Изменить": {
                "Отфильтровать данные": {
                    "onTriggered": self.checkFilter,
                    "checkable": True,
                    "icon": Icons["filter-files.svg"],
                    "objName": "filter",
                }
            },
        }

        self.selector = (
            None  # Объект селектора (таблицы из которой буду браться данные)
        )
        self.editor_enters = []  # Массив полей ввода данных
        self.menubar = QtWidgets.QMenuBar()
        self.editor_layout = QtWidgets.QGridLayout(
            self
        )  # Компоновщик в который поля добавляются
        MenuBarUtils.setupMenuBar(self.menubar, menubar_content, self)

    def openFile(self) -> None:
        print("openFile")

    def deleteFile(self) -> None:
        print("deleteFile")

    def getMenuBarCheckedState(self, name: str) -> bool:
        try:
            return self.menubar.findChildren(QtGui.QAction, name)[0].isChecked()
        except Exception as e:
            print(f"Что-то пошло не так. {e}")
            return False

    def showSaveFileDialog(self) -> None:
        dialog = SaveFileDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.directoryWorker.save_stroke_to_csv(
                dialog.getFullPath(), editor_content
            )

    def checkFilter(self) -> None:
        if self.getMenuBarCheckedState("filter"):
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.directoryWorker.update(editor_content, 0.5)
            self.selector.update()

    def update(self) -> None:
        if (
            self.editor_layout.isEmpty()
        ):  # Если в редакторе нет виджетов то добавляем их из файла TYPES
            self.editor_enters.clear()
            for i in range(len(self.directoryWorker.config_files["TYPES"])):
                widget = Units[
                    self.directoryWorker.config_files["TYPES"][i]
                ]()  # Создаем объект виджета (его берем из библиотеки inputs)
                widget.connectMethod(self.checkFilter)
                self.editor_enters.append(
                    widget
                )  # Добавляем его в массив полей ввода (для дальнейшей обработки)
                self.editor_layout.addWidget(widget, i, 1)  # Размещаем его в редакторе


class SaveFileDialog(QtWidgets.QDialog):
    def __init__(self, parent: FileEditor) -> None:
        super(SaveFileDialog, self).__init__()
        self.setWindowTitle("Сохранить файл в:")
        layout = QtWidgets.QGridLayout()
        self.pathField = QtWidgets.QLineEdit()
        self.pathField.setText(str(parent.directoryWorker.directory))
        layout.addWidget(QtWidgets.QLabel("Путь:"), 1, 0)
        layout.addWidget(self.pathField, 1, 1)
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def getFullPath(self) -> str:
        return self.pathField.text()
