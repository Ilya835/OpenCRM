from PyQt6 import QtWidgets, QtCore
import datetime

name = "Время"


class Time(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Передаваемые переменные:
    :param name: Имя виджета которое будет отображаться в QLabel
    :param format: Формат в котором в нем отображаются данные
    Методы:
    :param connectMethod: - присоединяет метод к изменению значения в QDoubleSpinbox
    :param getData: - возвращает данные из поля ввода
    :param setData: - устанавливает данные (автоматически конвертируя их в нужный тип)
    :param clearData: - очищает поле ввода
    """

    def __init__(self, name, formatString=None):
        super(Time, self).__init__()
        # Если formatString не передан то выставляем дефолтное значение
        if formatString is None:
            self.formatString = "dd.MM.yyyy hh:mm"  # Стандартный формат (полный номер дня:месяц цифрой:полный год часы:минуты)
        else:
            self.formatString = formatString
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(QtWidgets.QLabel(name), 0, 0)
        self.dataInput = QtWidgets.QDateTimeEdit()
        self.dataInput.setDisplayFormat(self.formatString)
        self.dataInput.setMinimumDateTime(QtCore.QDateTime(1993, 10, 4, 7, 0, 0))
        if "d" in self.formatString:
            self.dataInput.setCalendarPopup(True)
        self.layout.addWidget(self.dataInput, 0, 1)
        self.dataInput.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.dataInput.customContextMenuRequested.connect(self.addContextMenu)

    def convert_format(self, pyqt_format):
        """
        Конвертер форматов даты и времени.
        :param pyqt_format: формат который будет конвертироваться
        Внутри:
        :param format_mapping: возможные конвертации
        """
        format_mapping = {
            "HH": "%H",
            "H": "%H",
            "hh": "%I",
            "h": "%I",
            "mm": "%M",
            "ss": "%S",
            "AP": "%p",
            "ap": "%p",
            "yyyy": "%Y",
            "yy": "%y",
            "MM": "%m",
            "dddd": "%A",
            "ddd": "%a",
            "dd": "%d",
            ":": ":",
            ".": ".",
            "-": "-",
            "/": "/",
            " ": " ",
        }
        py_format = pyqt_format
        for qt, py in format_mapping.items():
            py_format = py_format.replace(qt, py)

        return py_format

    def setNowtime(self):
        """Выставляет текущее локальное время в dataInput"""
        self.setData(
            datetime.datetime.now().strftime(self.convert_format(self.formatString))
        )

    def addContextMenu(self, pos):
        """
        Метод добавляющий контекстное меню.
        :param contextMenuActions: list Массив состоящий из кортежей для действий в контекстном меню.
        """
        contextMenuActions = [
            ("Выставить текущее время", self.setNowtime),
            ("Очистить поле", self.clearData),
        ]
        menu = QtWidgets.QMenu(self)
        for text, handler in contextMenuActions:
            action = menu.addAction(text)
            action.triggered.connect(handler)
        menu.exec(self.dataInput.mapToGlobal(pos))

    def connectMethod(self, method):
        """Присоединяет переданный method к изменению значения в поле ввода (dataInput)"""
        self.dataInput.timeChanged.connect(method)

    def getData(self):
        """Получает данные из поля ввода (dataInput)
        :return: строка (str) с данными"""
        return self.dataInput.time().toString("hh:mm")

    def setData(self, data):
        """Устанавливает данные в поле ввода.
        :param data: любая переменная которая нормально преобразуется в строку.
        """
        self.dataInput.setDateTime(
            QtCore.QDateTime.fromString(str(data), self.formatString)
        )

    def clearData(self):
        """Выставляет дефолтное время"""
        self.dataInput.setDateTime(self.dataInput.minimumDateTime())
