from PyQt6 import QtGui, QtCore, QtWidgets


name = "Обзор папки"


class DirectoryExplorer(QtWidgets.QTableView):
    def __init__(self, directoryWorker):
        super().__init__()
        self.directoryWorker = directoryWorker
        self.setup_ui()
        self.set_data()

    def setup_ui(self):
        """ÐÐ°ÑÑÑÐ¾Ð¹ÐºÐ° Ð²Ð½ÐµÑÐ½ÐµÐ³Ð¾ Ð²Ð¸Ð´Ð° ÑÐ°Ð±Ð»Ð¸ÑÑ"""
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

    def set_data(self):
        model = DictArrayTableModel(
            self.directoryWorker.data_files, self.directoryWorker.config_files["HEADER"]
        )
        self.setModel(model)


class DictArrayTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data_dict, horizontal_headers):
        super().__init__()
        self.data_dict = data_dict
        self.horizontal_headers = horizontal_headers
        self.vertical_headers = list(data_dict.keys())
        self.column_types = self._detect_column_types()

        self._validate_data()

    def _detect_column_types(self):
        if not self.data_dict:
            return {}

        column_types = {}
        first_key = next(iter(self.data_dict))

        for col in range(len(self.data_dict[first_key])):
            sample_value = self.data_dict[first_key][col]

            if isinstance(sample_value, (QtGui.QPixmap, QtGui.QIcon)):
                column_types[col] = "image"
            elif isinstance(
                sample_value, (QtCore.QDateTime, QtCore.QDate, QtCore.QTime)
            ):
                column_types[col] = "datetime"
            elif isinstance(sample_value, (int, float)):
                column_types[col] = "number"
            elif isinstance(sample_value, bool):
                column_types[col] = "bool"
            else:
                column_types[col] = "text"

        return column_types

    def _validate_data(self):
        if not self.data_dict:
            return

        first_key = next(iter(self.data_dict))
        expected_length = len(self.data_dict[first_key])

        for key, values in self.data_dict.items():
            if len(values) != expected_length:
                raise ValueError(
                    f"Все массивы должны иметь одинаковую длинну."
                    f"Ключ '{key} имеет длинну {len(values)}, "
                    f"ожидается {expected_length}"
                )

        if len(self.horizontal_headers) != expected_length:
            raise ValueError(
                f"Количество горизонтальных заголовков ({len(self.horizontal_headers)}) "
                f"должно соответствовать длинне массивов ({expected_length})"
            )

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_dict)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if not self.data_dict:
            return 0
        return len(next(iter(self.data_dict.values())))

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        key = self.vertical_headers[row]
        value = self.data_dict[key][col]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if isinstance(value, (QtGui.QPixmap, QtGui.QIcon)):
                return None
            elif isinstance(value, (QtCore.QDateTime, QtCore.QDate, QtCore.QTime)):
                return self._format_datetime(value)
            elif isinstance(value, bool):
                return "ÐÐ°" if value else "ÐÐµÑ"
            else:
                return str(value)

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            if isinstance(value, (QtGui.QPixmap, QtGui.QIcon)):
                if isinstance(value, QtGui.QPixmap):
                    return QtGui.QIcon(value)
                return value
            return None

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if self.column_types.get(col) == "number":
                return (
                    QtCore.Qt.AlignmentFlag.AlignRight
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            elif self.column_types.get(col) == "datetime":
                return (
                    QtCore.Qt.AlignmentFlag.AlignCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            return (
                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
            )

        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return value

        return None

    def _format_datetime(self, dt, fmt):
        dt.toString(fmt)
        return str(dt)

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                if section < len(self.horizontal_headers):
                    return self.horizontal_headers[section]
            elif orientation == QtCore.Qt.Orientation.Vertical:
                if section < len(self.vertical_headers):
                    return self.vertical_headers[section]
        return None

    def flags(self, index):
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
