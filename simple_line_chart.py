# Example 3.1 from Modern PyQt Create GUI Application for Project Management, ...
# by Joshua Willman
# Example adapted for PySide6
import sys
import csv
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

class DisplayGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Ex 3.1 - Line Chart Example")

        self.setupChart()
        self.show()

    def setupChart(self):
        """
        Set up the GUI's graph line series type, chart instance, chart axes,
        and chart view widget.
        """
        # Collect x and y data vales from the CSV file
        x_values, y_values = self.loadCSVFile()

        # Create chart object
        chart = QChart()
        chart.setWindowTitle("Public Social Spending as a Share of GDP for Sweden, 1880 to 2016")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()

        line_series = QLineSeries()

        # Loop through corresponding x and y values and add to the line chart
        for value in range(0, self.row_count - 1):
            line_series.append(x_values[value], y_values[value])
        chart.addSeries(line_series)

        # Specify parameters for the x and y axes
        axis_x = QValueAxis()
        axis_x.setLabelFormat("%i")
        axis_x.setTickCount(10)
        axis_x.setRange(1880, 2016)
        chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i" + "%")
        axis_y.setRange(0, 40)
        chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)

        # Create QQhartView object for displaying the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Create layout and set the layout for the window
        v_box = QVBoxLayout()
        v_box.addWidget(chart_view)
        self.setLayout(v_box)


    def loadCSVFile(self):
        """
        Load data from CSV file for the line chart.
        Select and store x and y values into Python list objects.
        Return the x_values and y_values lists.
        """
        x_values, y_values = [], []
        file_name = "data/social_spending_sweden.csv"

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)

            for row in reader:
                x = int(row[2])
                x_values.append(x)
                y = float(row[3])
                y_values.append(y)

            # Count the number of rows in the CSV file. Reset the reader's current
            # position back to the beginning of the file.
            csv_f.seek(0)
            self.row_count = len(list(reader))

        return x_values, y_values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayGraph()
    sys.exit(app.exec())
