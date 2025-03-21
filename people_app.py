import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QMenuBar, QMenu,
    QPushButton, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QComboBox, QDialogButtonBox, QTextEdit
)
from PySide6.QtGui import QAction
from database_sqlite import Database
from people_repository import PeopleRepository


# --- PersonDialog for Adding/Editing a Person ---
class PersonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Person")
        self.layout = QFormLayout(self)

        # Create input fields.
        self.name_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.phone_edit = QLineEdit(self)
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["individual", "company"])
        self.company_name_edit = QLineEdit(self)
        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["active", "inactive"])
        self.notes_edit = QTextEdit(self)

        # Add fields to the form.
        self.layout.addRow("Name:", self.name_edit)
        self.layout.addRow("Email:", self.email_edit)
        self.layout.addRow("Phone:", self.phone_edit)
        self.layout.addRow("Type:", self.type_combo)
        self.layout.addRow("Company Name:", self.company_name_edit)
        self.layout.addRow("Status:", self.status_combo)
        self.layout.addRow("Notes:", self.notes_edit)

        # Dialog buttons.
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self):
        """Return a dictionary of the entered data."""
        return {
            "name": self.name_edit.text(),
            "email": self.email_edit.text() or None,
            "phone": self.phone_edit.text() or None,
            "person_type": self.type_combo.currentText(),
            "company_name": self.company_name_edit.text() or None,
            "status": self.status_combo.currentText(),
            "notes": self.notes_edit.text() or None
        }

    def set_data(self, data):
        self.name_edit.setText(data.get("name", ""))
        self.email_edit.setText(data.get("email", ""))
        self.phone_edit.setText(data.get("phone", ""))
        index = self.type_combo.findText(data.get("person_type", "individual"))
        self.type_combo.setCurrentIndex(index if index >= 0 else 0)
        self.company_name_edit.setText(data.get("company_name", ""))
        index = self.status_combo.findText(data.get("status", "active"))
        self.status_combo.setCurrentIndex(index if index >= 0 else 0)
        self.notes_edit.setText(data.get("notes", ""))

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

        # Table to display people id and name.
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Type", "Company Name", "Status", "Notes"])
        layout.addWidget(self.table)

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
        headers = ["ID", "Name", "Email", "Phone", "Type", "Company Name", "Status", "Notes", "Created At", "Updated At"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)

        for row_index, person in enumerate(people):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(person):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table.setItem(row_index, col_index, item)

    def get_selected_person_id(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # Assuming the first column holds the ID.
            return int(selected_items[0].text())
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
                notes=data["notes"]
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
            "notes": person[7]
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
                new_data["notes"]
            )
            self.load_people()

    def delete_person(self):
        person_id = self.get_selected_person_id()
        if person_id is None:
            QMessageBox.warning(self, "No Selection", "Please select a person to delete.")
            return
        confirm = QMessageBox.question(
            self, "Delete Person", "Are you sure you want to delete this person?",
            QMessageBox.Yes | QMessageBox.No
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
