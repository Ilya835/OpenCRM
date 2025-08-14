from .. import inputs
from PyQt6 import QtWidgets

name = "Редактор файла"


class FileEditor(QtWidgets.QGroupBox):
    def __init__(self, directoryWorker):
        super(FileEditor, self).__init__()
        self.directoryWorker = directoryWorker  # Объект менеджера папок
        self.selector = (
            None  # Объект селектора (таблицы из которой буду браться данные)
        )
        self.editor_enters = []  # Массив полей ввода данных
        self.editor_layout = QtWidgets.QGridLayout(
            self
        )  # Компоновщик в который поля добавляются

    def update(self):
        if (
            self.editor_layout.isEmpty()
        ):  # Если в редакторе нет виджетов то добавляем их из файла TYPES
            self.editor_enters.clear()
            for i in range(len(self.directoryWorker.files["TYPES"])):
                exist_check = (
                    lambda key, dictionary: dictionary[key][i]
                    if key in dictionary
                    else None
                )
                widget = inputs.content[self.directoryWorker.files["TYPES"][i]](
                    exist_check("HEADER", self.directoryWorker.files),
                    exist_check("FORMAT", self.directoryWorker.files),
                )  # Создаем объект виджета (его берем из библиотеки inputs)
                widget.connectMethod(
                    self.selector.update
                )  # Присоединяем к нему метод селектора "update"
                self.editor_enters.append(
                    widget
                )  # Добавляем его в массив полей ввода (для дальнейшей обработки)
                self.editor_layout.addWidget(widget, i, 1)  # Размещаем его в редакторе
        currentRowHeader = self.selector.verticalHeaderItem(self.selector.currentRow())
        if currentRowHeader is not None:
            self.setTitle(currentRowHeader.text())
            self.setDataFromFile(currentRowHeader.text())

    def setDataFromFile(self, filename):
        for i in range(len(self.editor_enters)):
            self.editor_enters[i].setData(self.directoryWorker.files[filename][i])
