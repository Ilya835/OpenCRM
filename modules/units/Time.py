from PyQt6 import QtWidgets, QtCore
import datetime

module_name = "Время"


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

    def __init__(
        self, name=module_name, formatString="dd.MM.yyyy hh:mm", isCheckable=False
    ):
        super(Time, self).__init__()
        self.formatString = formatString
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(QtWidgets.QLabel(name), 0, 0)
        self.dataInput = QtWidgets.QDateTimeEdit()
        self.dataInput.setDisplayFormat(formatString)
        self.dataInput.setMinimumDateTime(QtCore.QDateTime(1993, 10, 4, 7, 0, 0))
        self.dataInput.setDateTime(self.dataInput.minimumDateTime())
        if "d" in formatString:
            self.dataInput.setCalendarPopup(True)
        self.layout.addWidget(self.dataInput, 0, 1)
        self.dataInput.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.dataInput.customContextMenuRequested.connect(self.addContextMenu)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )
        self.setCheckable(isCheckable)

    def setNowDateTime(self):
        """Выставляет текущее локальное время в dataInput"""
        self.dataInput.setDateTime(datetime.datetime.now())

    def showDialog(self):
        dialog = TimeDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            dialog_ouput = dialog.getTime()
            new_time = QtCore.QDateTime(self.dataInput.dateTime())
            new_time.addDays(dialog_ouput[0])
            new_time.setTime(
                QtCore.QTime(
                    new_time.time().hour() + dialog_ouput[1],
                    new_time.time().second() + dialog_ouput[2],
                )
            )
            self.dataInput.setDateTime(new_time)

    def addContextMenu(self, pos):
        """
        Добавляет контекстное меню полю ввода.
        :param contextMenuActions: list Массив состоящий из кортежей для действий в контекстном меню.
        """
        contextMenuActions = [
            ("Выставить текущее время", self.setNowDateTime),
            ("Очистить поле", self.clearData),
            ("Прибавить время", self.showDialog),
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
        return self.dataInput.dateTime.toString("hh:mm")

    def setData(self, data):
        """Устанавливает данные в поле ввода.
        :param data: любая переменная которая нормально преобразуется в строку.
        """
        self.dataInput.setDateTime(data)

    def clearData(self):
        """Выставляет дефолтное время"""
        self.dataInput.setDateTime(self.dataInput.minimumDateTime())


class TimeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TimeDialog, self).__init__()
        self.setWindowTitle("Прибавить время.")
        layout = QtWidgets.QGridLayout()
        self.days = QtWidgets.QSpinBox()
        self.days.setMinimum(0)
        self.hours = QtWidgets.QSpinBox()
        self.hours.setMaximum(23)
        self.hours.setMinimum(0)
        self.minutes = QtWidgets.QSpinBox()
        self.minutes.setMaximum(59)
        self.minutes.setMinimum(0)
        layout.addWidget(QtWidgets.QLabel("Дней:"), 1, 0)
        layout.addWidget(self.days, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Часов:"), 2, 0)
        layout.addWidget(self.hours, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Минут:"), 3, 0)
        layout.addWidget(self.minutes, 3, 1)
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def getTime(self):
        return [self.days.value(), self.hours.value(), self.minutes.value()]
