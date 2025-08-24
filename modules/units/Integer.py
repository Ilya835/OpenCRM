from PyQt6 import QtWidgets

module_name = "Целое число"


class Integer(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Методы:
    connectMethod - присоединяет метод к изменению значения в QDoubleSpinbox
    getData - возвращает данные из поля ввода
    setData - устанавливает данные (автоматически конвертируя их в нужный тип)
    clearData - очищает поле ввода
    """

    def __init__(self, name=module_name, formatString=None, isCheckable=False):
        super(Integer, self).__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.setTitle(name)
        self.dataInput = QtWidgets.QSpinBox()
        self.dataInput.setSuffix(formatString)
        self.layout.addWidget(self.dataInput, 0, 1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )
        self.setCheckable(isCheckable)

    def connectMethod(self, method):
        self.dataInput.valueChanged.connect(method)

    def getData(self):
        return self.dataInput.value()

    def setData(self, data):
        self.dataInput.setValue(int(data))

    def clearData(self):
        self.dataInput.clear()
