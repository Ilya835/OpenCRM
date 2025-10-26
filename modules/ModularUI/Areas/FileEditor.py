import sys
from PyQt6 import QtWidgets, QtGui, QtCore
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
from content.icons import Icons
from modules.Misc import MenuUtils, DirectoryManager
from modules.ModularUI.Areas import DirectoryExplorer
from modules.ModularUI import Units


class FileEditor(QtWidgets.QScrollArea):
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
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        self.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        MenuUtils.setupMenuBar(MenuUtils, self.menubar, menubar_content, self.scrollAreaWidgetContents)
        self.update_data()

    def openFile(self) -> None:
        filename, ok = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберете файл", str(Path.home()), "Data files (*.DAT)"
        )
        if filename:
            path = Path(filename)
            try:
                self.DirManager.directory = path.parent
                self.DirManager.update_files()
            except:
                pass
            print(self.DirManager.config_file)
            self.setTitle(str(self.DirManager.directory))
            self.update_data()
            self.selector.update_data()

    def deleteFile(self) -> None:
        print("deleteFile")

    def getMenuBarCheckedState(self, name: str) -> bool:
        try:
            return self.menubar.findChildren(QtGui.QAction, name)[0].isChecked()
        except Exception as e:
            print(f"Что-то пошло не так. {e}")
            return False

    def showSaveFileDialog(self) -> None:
        def getPath():
            filename, ok = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Выберете файл",
                str(self.DirManager.directory),
                "Data file (*.DAT)",
            )
            if filename:
                return (
                    str(Path(filename))
                    if filename.endswith(".DAT")
                    else str(Path(filename + ".DAT"))
                )
            else:
                return str(None)

        editor_content = []
        for i in self.editor_enters:
            editor_content.append(i.getData())
        self.DirManager.file_loader.save_file(getPath(), editor_content)
        self.DirManager.update_files()
        self.selector.update_data()

    def checkFilter(self) -> None:
        if self.getMenuBarCheckedState("filter"):
            editor_content = []
            for i in self.editor_enters:
                editor_content.append(i.getData())
            self.DirManager.update(editor_content, 0.5)
            self.selector.update()

    def update_data(self) -> None:
        for i in self.editor_enters:
            i.deleteLater()
        if True:  # Если в редакторе нет виджетов то добавляем их из файла TYPES
            self.editor_enters.clear()
            for i in self.DirManager.config_file:
                if i["unit"] == "Картинка":
                    widget = Units.PixmapGroupBox(self)
                elif i["unit"] == "Ссылка на внешний файл данных":
                    widget = Units.DataComboBox(i["dataSource"], self)
                else:
                    widget = Units.CustomGroupBox(
                        i["unit"]
                    )  # Создаем объект виджета (его берем из библиотеки inputs)

                widget.connectMethod(self.checkFilter)
                widget.setTitle(i["header"])
                self.editor_enters.append(
                    widget
                )  # Добавляем его в массив полей ввода (для дальнейшей обработки)
                self.scrollAreaWidgetContents.layout().addWidget(widget)  # Размещаем его в редакторе


MainClass = FileEditor
