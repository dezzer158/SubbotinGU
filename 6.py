import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLabel, QComboBox, QFileDialog, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ данных и визуализация")
        self.data = None

        self.init_ui()

    def init_ui(self):

        main_widget = QWidget()
        layout = QVBoxLayout()


        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        self.stats_label = QLabel("Статистика:")
        layout.addWidget(self.stats_label)


        self.chart_selector = QComboBox()
        self.chart_selector.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])
        self.chart_selector.currentIndexChanged.connect(self.update_chart)
        layout.addWidget(self.chart_selector)


        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def load_data(self):

        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV-файл", "", "CSV Files (*.csv)")
        if file_path:
            self.data = pd.read_csv(file_path)
            self.update_stats()
            self.update_chart()

    def update_stats(self):
        if self.data is not None:
            stats = f"Количество строк: {self.data.shape[0]}\n"
            stats += f"Количество столбцов: {self.data.shape[1]}\n"
            stats += f"Минимальные значения:\n{self.data.min()}\n"
            stats += f"Максимальные значения:\n{self.data.max()}\n"
            self.stats_label.setText(stats)

    def update_chart(self):
        if self.data is not None:
            chart_type = self.chart_selector.currentText()
            self.ax.clear()

            if chart_type == "Линейный график":
                self.data.plot(x="Date", y="Value1", ax=self.ax, kind="line")
            elif chart_type == "Гистограмма":
                self.data.plot(x="Date", y="Value2", ax=self.ax, kind="bar")
            elif chart_type == "Круговая диаграмма":
                if "Category" in self.data.columns:
                    self.data["Category"].value_counts().plot.pie(ax=self.ax, autopct="%1.1f%%")

            self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataVisualizer()
    window.show()
    sys.exit(app.exec_())
