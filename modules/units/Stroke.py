from PyQt6 import QtWidgets

module_name = "Строка"


class Stroke(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Методы:
    connectMethod - присоединяет метод к изменению значения в QDoubleSpinbox
    getData - возвращает данные из поля ввода
    setData - устанавливает данные (автоматически конвертируя их в нужный тип)
    clearData - очищает поле ввода
    """

    def __init__(self, name=module_name, formatString=None, isCheckable=False):
        super(Stroke, self).__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.setTitle(name)
        self.dataInput = QtWidgets.QLineEdit()
        self.dataInput.setInputMask(formatString)
        self.layout.addWidget(self.dataInput, 0, 1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )
        self.setCheckable(isCheckable)

    def connectMethod(self, method):
        self.dataInput.textChanged.connect(method)

    def getData(self):
        return self.dataInput.text()

    def setData(self, data):
        self.dataInput.setText(str(data))

    def clearData(self):
        self.dataInput.clear()
