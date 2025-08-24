from ..units import Units
from ..icons import Icons
from PyQt6 import QtWidgets, QtGui, QtCore

name = "Редактор файла"


class FileEditor(QtWidgets.QGroupBox):
    def __init__(self, directoryWorker):
        super(FileEditor, self).__init__()
        self.directoryWorker = directoryWorker  # Объект менеджера папок
        self.selector = (
            None  # Объект селектора (таблицы из которой буду браться данные)
        )
        self.editor_enters = []  # Массив полей ввода данных
        self.menubar = QtWidgets.QMenuBar()
        self.editor_layout = QtWidgets.QGridLayout(
            self
        )  # Компоновщик в который поля добавляются
        self.setupMenuBar()
        self.editor_layout.setMenuBar(self.menubar)

    def openFile(self):
        print("openFile")
        pass

    def saveFile(self):
        print("saveFile")
        pass

    def deleteFile(self):
        print("deleteFile")
        pass

    def getMenuBarCheckedState(self, name):
        try:
            return self.menubar.findChildren(QtGui.QAction, name="filter")[
                0
            ].isChecked()
        except Exception as e:
            print(f"Что-то пошло не так. {e}")

    def showDialog(self):
        dialog = SaveFileDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.directoryWorker.save_stroke_to_csv(
                dialog.getFullPath(), editor_content
            )

    def setupMenuBar(self):
        menubar_content = {
            "Файл": {
                "Открыть": {
                    "onTriggered": self.openFile,
                    "checkable": False,
                    "icon": Icons["open-file.svg"],
                    "objName": "open",
                },
                "separator": None,
                "Сохранить": {
                    "onTriggered": self.showDialog,
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
        for i in list(menubar_content.keys()):
            menu = QtWidgets.QMenu(i, self.menubar)
            for j in list(menubar_content[i].keys()):
                if j == "separator":
                    menu.addSeparator()
                else:
                    action = QtGui.QAction(j, menu)
                    action.triggered.connect(menubar_content[i][j]["onTriggered"])
                    action.setCheckable(menubar_content[i][j]["checkable"])
                    action.setIcon(menubar_content[i][j]["icon"])
                    action.setObjectName(menubar_content[i][j]["objName"])
                    menu.addAction(action)
            self.menubar.addMenu(menu)
            menu.show()

    def checkFilter(self):
        if self.getMenuBarCheckedState("filter"):
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.directoryWorker.update(editor_content, 0.5)
            self.selector.update()

    def update(self):
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
        # currentRowHeader = self.selector.verticalHeaderItem(self.selector.currentRow())
        # if currentRowHeader is not None:
        #    self.setTitle(currentRowHeader.text())


class SaveFileDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SaveFileDialog, self).__init__()
        self.setWindowTitle("Сохранить файл в:")
        layout = QtWidgets.QGridLayout()
        self.pathField = QtWidgets.QLineEdit()
        self.pathField.setText(parent.directoryWorker.directory)
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

    def getFullPath(self):
        return self.pathField.text()
