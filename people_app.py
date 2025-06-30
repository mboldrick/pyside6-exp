import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QTableView,
    QTableWidgetItem,
    QMenuBar,
    QMenu,
    QPushButton,
    QMessageBox,
    QDialog,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QAbstractTableModel
from database_sqlite import Database
from people_repository import PeopleRepository
from person_dialog import PersonDialog


class PeopleTableModel(QAbstractTableModel):
    def __init__(self, people, headers, parent=None):
        super().__init__(parent)
        self.people = people
        self.headers = headers

    def rowCount(self, parent=None):
        return len(self.people)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            person = self.people[index.row()]
            value = person[index.column()]
            return str(value) if value is not None else ""
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            else:
                return str(section)
        return None


# --- PySide6 Main App ---
class MainWindow(QMainWindow):
    def __init__(self, db, people_repo):
        super().__init__()
        self.db = db
        self.people_repo = people_repo
        self.setWindowTitle("Billing and Accounting App")
        self.resize(1024, 768)

        self.setup_menu()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.people_tab = QWidget()
        self.tabs.addTab(self.people_tab, "People")
        self.setup_people_tab()
        self.load_people()

    def setup_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        people_menu = menu_bar.addMenu("People")

        list_action = QAction("List People", self)
        list_action.triggered.connect(self.load_people)
        people_menu.addAction(list_action)

        add_action = QAction("Add Person", self)
        add_action.triggered.connect(self.add_person)
        people_menu.addAction(add_action)

        edit_action = QAction("Edit Person", self)
        edit_action.triggered.connect(self.edit_person)
        people_menu.addAction(edit_action)

        delete_action = QAction("Delete Person", self)
        delete_action.triggered.connect(self.delete_person)
        people_menu.addAction(delete_action)

    def setup_people_tab(self):
        layout = QVBoxLayout()
        self.people_tab.setLayout(layout)

        # Table to display people.
        # Using QTableView instead of QTableWidget.
        self.table = QTableView()
        layout.addWidget(self.table)
        # self.table.setColumnCount(8)
        # self.table.setHorizontalHeaderLabels(
        #     ["ID", "Name", "Email", "Phone", "Type", "Company Name", "Status", "Notes"]
        # )
        # layout.addWidget(self.table)

        # Buttons for actions.
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_person)
        button_layout.addWidget(add_btn)

        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_person)
        button_layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_person)
        button_layout.addWidget(delete_btn)

    def load_people(self):
        # Fetch all columns from the people table.
        people = self.people_repo.list_people()
        headers = [
            "ID",
            "Name",
            "Email",
            "Phone",
            "Type",
            "Company Name",
            "Status",
            "Notes",
            "Created At",
            "Updated At",
        ]
        model = PeopleTableModel(people, headers)
        self.table.setModel(model)

    def get_selected_person_id(self):
        selected_indexes = self.table.selectionModel().selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            model = self.table.model()
            index = model.index(row, 0)
            return int(model.data(index))
        else:
            return None

    def add_person(self):
        # Use the custom dialog to collect person information.
        dialog = PersonDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Missing Name", "Name is required!")
                return
            self.people_repo.create_person(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                person_type=data["person_type"],
                company_name=data["company_name"],
                status=data["status"],
                notes=data["notes"],
            )
            self.load_people()

    def edit_person(self):
        person_id = self.get_selected_person_id()
        if person_id is None:
            QMessageBox.warning(self, "No Selection", "Please select a person to edit.")
            return

        # Fetch full person details from the database.
        person = self.people_repo.get_person(person_id)
        if not person:
            QMessageBox.warning(self, "Error", "Person not found in database.")
            return

        # Map the fetched data into a dictionary.
        # Assuming person tuple is:
        # (id, name, email, phone, type, company_name, status, notes, created_at, updated_at)
        data = {
            "name": person[1],
            "email": person[2],
            "phone": person[3],
            "person_type": person[4],
            "company_name": person[5],
            "status": person[6],
            "notes": person[7],
        }

        # Create the dialog and pre-populate fields.
        dialog = PersonDialog(self)
        dialog.set_data(data)  # You need to implement this method in PersonDialog.

        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_data()
            self.people_repo.update_person(
                person_id,
                new_data["name"],
                new_data["email"],
                new_data["phone"],
                new_data["person_type"],
                new_data["company_name"],
                new_data["status"],
                new_data["notes"],
            )
            self.load_people()

    def delete_person(self):
        person_id = self.get_selected_person_id()
        if person_id is None:
            QMessageBox.warning(
                self, "No Selection", "Please select a person to delete."
            )
            return
        confirm = QMessageBox.question(
            self,
            "Delete Person",
            "Are you sure you want to delete this person?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.people_repo.delete_person(person_id)
            self.load_people()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize the database and repository (using SQLite).
    db = Database("billing.db")
    people_repo = PeopleRepository(db)

    window = MainWindow(db, people_repo)
    window.show()
    sys.exit(app.exec())
