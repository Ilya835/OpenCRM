from PyQt6 import QtGui, QtCore
from typing import Any

module_name = "Обрабатываемый QPixmap"


class PickablePixmap(QtGui.QPixmap):
    def __reduce__(self) -> Any:
        return type(self), (), self.__getstate__()

    def __getstate__(self) -> QtCore.QByteArray:
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.OpenModeFlag.WriteOnly)
        stream << self
        return ba

    def __setstate__(self, ba: QtCore.QByteArray) -> None:
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.OpenModeFlag.ReadOnly)
        stream >> self
