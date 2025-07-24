from PyQt6 import QtWidgets

name = "Дробное число"


class Float(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Методы:
    connectMethod - присоединяет метод к изменению значения в QDoubleSpinbox
    getData - возвращает данные из поля ввода
    setData - устанавливает данные (автоматически конвертируя их в нужный тип)
    clearData - очищает поле ввода
    """

    def __init__(self, name):
        super(Float, self).__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(QtWidgets.QLabel(name), 0, 0)
        self.dataInput = QtWidgets.QDoubleSpinBox()
        self.layout.addWidget(self.dataInput, 0, 1)

    def connectMethod(self, method):
        self.dataInput.valueChanged.connect(method)

    def getData(self):
        return self.dataInput.value()

    def setData(self, data):
        self.dataInput.setText(float(data))

    def clearData(self):
        self.dataInput.clear()
