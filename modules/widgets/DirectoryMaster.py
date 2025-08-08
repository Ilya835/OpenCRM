from PyQt6 import QtWidgets


class DirectoryMaster(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.layout().addWidget(QtWidgets.QLabel("TEST"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = DirectoryMaster()
    window.show()
    app.exec()
