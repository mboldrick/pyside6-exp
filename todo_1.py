import json
from pathlib import Path
import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc

from MainWindow import Ui_MainWindow

BASE_DIR = Path(__file__).resolve().parent

tick = qtg.QImage(str(BASE_DIR / "images" / "tick.png"))

class TodoModel(qtc.QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == qtc.Qt.DisplayRole:
            status, text = self.todos[index.row()]
            return text

        if role == qtc.Qt.DecorationRole:
            status, text = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.model = TodoModel(todos=[(False, "Item 1"), (True, "Item 2")])
        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)
        # Connect the buttons to methods.
        self.addButton.pressed.connect(self.add)
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton.pressed.connect(self.complete)

    def add(self):
        """
        Add a new item to the todo list, getting the text from the QLineEdit, todoEdit,
        then clearing it.
        """
        text = self.todoEdit.text()
        # Remove whitespace from the ends of the string
        text = text.strip()
        if text: # Don't add empty strings
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input.
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        """
        Delete the selected item from the todo list.
        """
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # indexes is a single-item list in single-select mode.
            index = indexes[0]
            # Remove the item and refresh
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clearn the selection (as it's no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        """
        Mark the selected item as complete.
        """
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            # Get the current status and text
            status, text = self.model.todos[row]
            # Replace the item with the same text, but opposite status.
            self.model.todos[row] = (not status, text)
            # Refresh the view. For a single selection, .dataChanged takes top-left and bottom-right, which are the same.
            self.model.dataChanged.emit(index, index)
            # Clear the selection.
            self.todoView.clearSelection()
            self.save()

    def load(self):
        """
        Load the todo list from a JSON file.
        """
        try:
            with open("todos.json", "r") as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open("todos.json", "w") as f:
            data = json.dump(self.model.todos, f)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
