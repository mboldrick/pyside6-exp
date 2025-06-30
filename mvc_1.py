import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFormLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
)

model = {
    "name": "Johnina Smith",
    "age": 30,
    "favorite_color": "blue",
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MVC Example")

        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setText(model["name"])
        self.name.textChanged.connect(self.handle_name_changed)

        self.age = QSpinBox()
        self.age.setRange(0, 120)
        self.age.setValue(model["age"])
        self.age.valueChanged.connect(self.handle_age_changed)

        self.fav_color = QComboBox()
        self.fav_color.addItems(["red", "green", "blue", "yellow"])
        self.fav_color.setCurrentText(model["favorite_color"])
        self.fav_color.currentTextChanged.connect(self.handle_fav_color_changed)

        self.save_btn = QPushButton("Save")
        self.restore_btn = QPushButton("Restore")

        layout.addRow("Name:", self.name)
        layout.addRow("Age:", self.age)
        layout.addRow("Favorite Color:", self.fav_color)
        layout.addRow(self.save_btn, self.restore_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_name_changed(self, text):
        model["name"] = text
        print(model)

    def handle_age_changed(self, value):
        model["age"] = value
        print(model)

    def handle_fav_color_changed(self, text):
        model["favorite_color"] = text
        print(model)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
