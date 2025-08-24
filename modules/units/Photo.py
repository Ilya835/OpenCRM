from PyQt6 import QtWidgets, QtGui

module_name = "Фото"


class Photo(QtWidgets.QGroupBox):
    """
    Класс поля записи (интерфейс Qt6)
    Методы:
    connectMethod - присоединяет метод к изменению значения в QDoubleSpinbox
    getData - возвращает данные из поля ввода
    setData - устанавливает данные (автоматически конвертируя их в нужный тип)
    clearData - очищает поле ввода
    """

    def __init__(self, name=module_name, formatString=None):
        super(Photo, self).__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.setTitle(name)
        self.dataInput = QtWidgets.QLabel(self)
        self.layout.addWidget(self.dataInput, 0, 1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )
        self.setData("/home/ilya/Projects/OpenCRM/content/photo_placeholder.png")

    def connectMethod(self, method):
        pass

    def getData(self):
        pass

    def setData(self, data):
        picture = QtGui.QPixmap(str(data))
        self.dataInput.setPixmap(picture)

    def clearData(self):
        pass
