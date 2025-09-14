import random
import sys

from collections import UserDict

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFormLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QCheckBox,
)
from PySide6.QtCore import QObject, Signal


class DataModelSignals(QObject):
    """Signals for the data model."""

    # Emit an "updated" signal when a property changes.
    updated = Signal()


class DataModel(UserDict):
    """A simple data model that extends UserDict to hold our data."""

    def __init__(self, *args, **kwargs):
        self.signals = DataModelSignals()
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """Override to emit a signal when the model is updated."""
        previous = self.get(key)  # Get the existing value.
        super().__setitem__(key, value)  # Set the value.
        if value != previous:  # There is a change.
            self.signals.updated.emit()  # Emit the signal.
            print(self)  # Show the current state.


model = DataModel(
    name="Johnina Smith",
    age=30,
    favorite_color="blue",
    disable_details=False,
)

# Store backups as a simple list of dictionaries.
backups = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MVC Example")

        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.textChanged.connect(self.handle_name_changed)

        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.valueChanged.connect(self.handle_age_changed)

        self.fav_color = QComboBox()
        self.fav_color.addItems(["red", "green", "blue", "yellow"])
        self.fav_color.currentTextChanged.connect(self.handle_fav_color_changed)

        self.save_btn = QPushButton("Save")
        self.save_btn.pressed.connect(self.handle_save_btn)

        self.restore_btn = QPushButton("Restore")
        self.restore_btn.pressed.connect(self.handle_restore_btn)

        self.disable_details = QCheckBox("Disable details")
        self.disable_details.toggled.connect(self.handle_disable_details)

        layout.addRow("Name:", self.name)
        layout.addRow("Age:", self.age)
        layout.addRow("Favorite Color:", self.fav_color)
        layout.addWidget(self.disable_details)
        layout.addRow(self.save_btn, self.restore_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_ui()
        # Hok our UI sync into the model's updated signal.
        model.signals.updated.connect(self.update_ui)

    def update_ui(self):
        """Synchronize the UI with the current model state."""
        self.name.setText(model["name"])
        self.age.setValue(model["age"])
        self.fav_color.setCurrentText(model["favorite_color"])
        self.disable_details.setChecked(model["disable_details"])

        # Enable/disable fields based on the state of disable_details.
        self.age.setDisabled(model["disable_details"])
        self.fav_color.setDisabled(model["disable_details"])

    def handle_name_changed(self, text):
        model["name"] = text

    def handle_age_changed(self, value):
        model["age"] = value

    def handle_fav_color_changed(self, text):
        model["favorite_color"] = text

    def handle_disable_details(self, checked):
        model["disable_details"] = checked

    def handle_save_btn(self):
        # Save a copy of the current model (if we don't copy changes will modify the backup!)
        backups.append(model.copy())
        print("SAVE:", model)
        print("BACKUPS:", len(backups))

    def handle_restore_btn(self):
        # Randomly get a backup.
        if not backups:
            return  # Ignore if empty.
        random.shuffle(backups)
        backup = backups.pop()
        model.update(backup)
        print("RESTORE:", model)
        print("BACKUPS:", len(backups))


app = QApplication(sys.argv)
window_a = MainWindow()
window_a.show()

# window_b = MainWindow()
# window_b.show()

app.exec()
