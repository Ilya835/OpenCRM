from PyQt6 import QtCore, QtGui
from typing import Any
class PickablePixmap(QtGui.QPixmap):
    """
    Класс для полноценной работы с QPixmap (избегает ошибки QPixmap object is not pickable)
    """

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
MainClass = PickablePixmap
