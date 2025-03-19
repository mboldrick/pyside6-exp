import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QMenuBar, QMenu,
    QPushButton, QInputDialog, QMessageBox
)
from PySide6.QtGui import QAction
from database_sqlite import Database
from people_repository import PeopleRepository

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
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Name"])
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
        people = self.people_repo.list_people()
        self.table.setRowCount(0)
        for row_index, (person_id, name) in enumerate(people):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(str(person_id)))
            self.table.setItem(row_index, 1, QTableWidgetItem(name))

    def get_selected_person_id(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # Assuming the first column holds the ID.
            return int(selected_items[0].text())
        else:
            return None

    def add_person(self):
        name, ok = QInputDialog.getText(self, "Add Person", "Enter name:")
        if ok and name:
            self.people_repo.create_person(name)
            self.load_people()

    def edit_person(self):
        person_id = self.get_selected_person_id()
        if person_id is None:
            QMessageBox.warning(self, "No Selection", "Please select a person to edit.")
            return
        # Fetch current name from the selected row.
        row = self.table.currentRow()
        current_name = self.table.item(row, 1).text() if row != -1 else ""
        name, ok = QInputDialog.getText(self, "Edit Person", "Edit name:", text=current_name)
        if ok and name:
            self.people_repo.update_person(person_id, name)
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
