from PyQt6 import QtWidgets

name = "Целое число"


class Integer(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Методы:
    connectMethod - присоединяет метод к изменению значения в QDoubleSpinbox
    getData - возвращает данные из поля ввода
    setData - устанавливает данные (автоматически конвертируя их в нужный тип)
    clearData - очищает поле ввода
    """

    def __init__(self, name, formatString=None):
        super(Integer, self).__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(QtWidgets.QLabel(name), 0, 0)
        self.dataInput = QtWidgets.QSpinBox()
        if formatString:
            self.formatString = formatString
            self.dataInput.setSuffix(self.formatString)
        self.layout.addWidget(self.dataInput, 0, 1)

    def connectMethod(self, method):
        self.dataInput.valueChanged.connect(method)

    def getData(self):
        return self.dataInput.value()

    def setData(self, data):
        self.dataInput.setValue(int(data))

    def clearData(self):
        self.dataInput.clear()
