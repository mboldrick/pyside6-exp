import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QWebEngineView widget
        self.web_view = QWebEngineView()

        # Load a local HTML file
        local_html_file = "path/to/your/localfile.html"  # Replace with your file path
        self.web_view.load(QUrl.fromLocalFile(local_html_file))

        # Set the QWebEngineView widget as the central widget
        self.setCentralWidget(self.web_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
