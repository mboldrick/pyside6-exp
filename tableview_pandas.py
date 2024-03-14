import sys

import pandas as pd
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc


class TableModel(qtc.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == qtc.Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == qtc.Qt.DisplayRole:
            if orientation == qtc.Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == qtc.Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = qtw.QTableView()

        data = pd.DataFrame(
            [
                [1, 9, 2],
                [1, 0, -1],
                [3, 5, 2],
                [3, 3, 2],
                [5, 8, 9],
            ],
            columns = ["A", "B", "C"],
            index = ["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"],
        )

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
        self.setGeometry(600, 100, 400, 200)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
