from PyQt6 import QtWidgets

name = "Обзор папки"


class DirectoryExplorer(QtWidgets.QTableWidget):
    def __init__(self, directoryWorker):
        super(DirectoryExplorer, self).__init__()
        self.directoryWorker = directoryWorker
        self.enters = None
        self.filtering = False
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    def update(self):
        self.directoryWorker.update()
        if (self.enters is not None) and self.filtering:
            enters_content = []
            for i in self.enters.editor_enters:
                enters_content.append(str(i.getData()))
            self.directoryWorker.update(
                filename_filter=None, data_filter=enters_content
            )
        self.itemSelectionChanged.connect(self.enters.update)
        self.setColumnCount(len(self.directoryWorker.files["HEADER"]))
        self.setHorizontalHeaderLabels(self.directoryWorker.files["HEADER"])
        self.setRowCount(
            len(
                list(filter(lambda x: x.find(".DAT") != -1, self.directoryWorker.files))
            )
        )
        self.setVerticalHeaderLabels(self.directoryWorker.files.keys())
        for i in range(
            len(
                list(filter(lambda x: x.find(".DAT") != -1, self.directoryWorker.files))
            )
        ):
            for j in range(len(list(self.directoryWorker.files["HEADER"]))):
                self.setItem(
                    i,
                    j,
                    QtWidgets.QTableWidgetItem(
                        str(list(self.directoryWorker.files.values())[i][j])
                    ),
                )
