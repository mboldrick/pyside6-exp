from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QDialogButtonBox,
)


class PersonDialog(QDialog):
    """Dialog for adding or editing a person."""

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
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
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
            "notes": self.notes_edit.toPlainText() or None,
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
        self.notes_edit.setPlainText(data.get("notes", ""))
