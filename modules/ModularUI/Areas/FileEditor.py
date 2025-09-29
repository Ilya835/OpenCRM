import sys
from PyQt6 import QtWidgets, QtGui
from typing import Any, Dict, Union, List
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
from modules.icons import Icons
from modules.Misc import MenuUtils, DirectoryManager
from modules.ModularUI.Areas import DirectoryExplorer
from modules.ModularUI import Units


class FileEditor(QtWidgets.QGroupBox):
    def __init__(
        self,
        DirManager: DirectoryManager,
    ):
        super(FileEditor, self).__init__()
        self.DirManager = DirManager  # Объект менеджера папки
        menubar_content: Dict[str, List[Union[MenuUtils.MenuItem, None]]] = {
            "Файл": [
                MenuUtils.MenuItem(
                    "Открыть", self.openFile, False, Icons["open-file.svg"], "open"
                ),
                None,
                MenuUtils.MenuItem(
                    "Сохранить",
                    self.showSaveFileDialog,
                    False,
                    Icons["save-file.svg"],
                    "save",
                ),
                MenuUtils.MenuItem(
                    "Удалить", self.deleteFile, False, Icons["trashbox.svg"], "remove"
                ),
            ],
            "Изменить": [
                MenuUtils.MenuItem(
                    "Отфильтровать данные",
                    self.checkFilter,
                    True,
                    Icons["filter-files.svg"],
                    "filter",
                ),
            ],
        }

        self.selector: Union[DirectoryExplorer.DirectoryExplorer, None]
        self.editor_enters: list[Any] = []  # Массив полей ввода данных
        self.menubar = QtWidgets.QMenuBar()
        self.setLayout(QtWidgets.QGridLayout(self))
        MenuUtils.setupMenuBar(self.menubar, menubar_content, self)

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
            self.DirManager.save_stroke_to_csv(dialog.getFullPath(), editor_content)

    def checkFilter(self) -> None:
        if self.getMenuBarCheckedState("filter"):
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.DirManager.update(editor_content, 0.5)
            self.selector.update()

    def update(self) -> None:
        if (
            self.layout().isEmpty()
        ):  # Если в редакторе нет виджетов то добавляем их из файла TYPES
            self.editor_enters.clear()
            for i in range(len(self.DirManager.config_files["TYPES"])):
                widget = Units.CustomGroupBox(
                    self.DirManager.config_files["TYPES"][i]
                )  # Создаем объект виджета (его берем из библиотеки inputs)
                widget.connectMethod(self.checkFilter)
                widget.setTitle(self.DirManager.config_files["HEADER"][i])
                self.editor_enters.append(
                    widget
                )  # Добавляем его в массив полей ввода (для дальнейшей обработки)
                self.layout().addWidget(widget, i, 1)  # Размещаем его в редакторе


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
MainClass = FileEditor
