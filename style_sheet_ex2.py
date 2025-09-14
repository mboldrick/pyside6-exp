import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

style_sheet = """
    QPushButton#Warning_Button {
        background-color: #C92108;
        broder-radius: 5px;
        padding: 6px;
        color: #FFFFFF
    }
    QPushButton#Warning_Button:pressed {
        background-color: #F4B519;
    }
"""


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        """Set up the application's GUI"""
        self.setMinimumSize(230, 140)
        self.setWindowTitle("Style Sheet Example 2")

        label = QLabel("<p align-center>Push a button.</p>")
        normal_button = QPushButton("Normal")
        warning_button = QPushButton("Warning!")
        # Set ID Selector
        warning_button.setObjectName("Warning_Button")

        v_box = QVBoxLayout()
        v_box.addWidget(label)
        v_box.addWidget(normal_button)
        v_box.addWidget(warning_button)

        self.setLayout(v_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
