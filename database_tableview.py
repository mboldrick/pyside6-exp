from pathlib import Path
import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc
from PySide6 import QtSql as qts

BASE_DIR = Path(__file__).resolve().parent


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Table View")
        self.setGeometry(100, 100, 1024, 600)
        self.setMinimumSize(qtc.QSize(1024, 600))

        self.table = qtw.QTableView()

        self.createConnection()

        self.model = qts.QSqlTableModel(db=self.db)
        self.table.setModel(self.model)
        self.model.setTable("Track")
        self.model.select()

        self.setCentralWidget(self.table)

    def createConnection(self):
        """Create a connection to the database."""
        self.db = qts.QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(str(BASE_DIR / "chinook.sqlite"))

        if not self.db.open():
            qtw.QMessageBox.critical(
                None,
                "Cannot open database",
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read the Qt SQL "
                "driver documentation for information how to build it.\n\n"
                "Click Cancel to exit.",
                qtw.QMessageBox.Cancel,
            )
            return False

        return True


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
