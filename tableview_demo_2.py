import sys
from datetime import datetime
from pathlib import Path

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc

BASE_DIR = Path(__file__).resolve().parent

# Icons used in cells
calendar = qtg.QImage(str(BASE_DIR / "images" / "calendar.png"))
cross = qtg.QImage(str(BASE_DIR / "images" / "cross.png"))
tick = qtg.QImage(str(BASE_DIR / "images" / "tick.png"))

# Color range -5 to +5; 0 = light gray
COLORS = ['#053051', '#2166ac', '#4393c3', '#92c5d3', '#d1e5f0', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']


class TableModel(qtc.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == qtc.Qt.DisplayRole:
            # Get the value.
            value = self._data[index.row()][index.column()]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")

            # Default (antything not caught above: e.g. int)
            return value

        if role == qtc.Qt.DecorationRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return calendar
            if isinstance(value, bool):
                if value:
                    return tick
                return cross
            if isinstance(value, int) or isinstance(value, float):
                value = int(value)

                # Limit to range -5 to +5; then conver to 0...10.
                value = max(-5, value) # values < -5 become -5
                value = min(5, value) # values > +5 become +5
                value = value + 5 # shift to 0...10

                return qtg.QColor(COLORS[value])

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The length of the first inner list
        return len(self._data[0])


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = qtw.QTableView()

        data = [
            [True, 9, 2],
            [1, -1, 'hello'],
            [3.027, False, -5],
            [3, 3, datetime(1959,9,22)],
            [7.555, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
