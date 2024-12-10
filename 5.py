import sys
import time
import requests
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer


class DataLoadThread(QThread):
    data_loaded = pyqtSignal(list)

    def run(self):
        try:

            time.sleep(2)
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            if response.status_code == 200:
                posts = response.json()
   
                self.data_loaded.emit(posts)
            else:
                self.data_loaded.emit([])
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.data_loaded.emit([])


class DataSaveThread(QThread):
    data_saved = pyqtSignal(list)

    def __init__(self, posts, parent=None):
        super().__init__(parent)
        self.posts = posts

    def run(self):
        try:

            time.sleep(2)
            conn = sqlite3.connect("posts.db")
            c = conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                title TEXT,
                body TEXT
            )
            """)

            c.execute("DELETE FROM posts")
            for p in self.posts:
                c.execute(
                    "INSERT INTO posts (id, userId, title, body) VALUES (?, ?, ?, ?)",
                    (p['id'], p['userId'], p['title'], p['body'])
                )
            conn.commit()
            conn.close()
            self.data_saved.emit(self.posts)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
            self.data_saved.emit([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронное обновление данных")


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "UserID", "Title", "Body"])


        self.load_button = QPushButton("Загрузить данные вручную")
        self.load_button.clicked.connect(self.on_load_data)


        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.table)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)


        self.timer = QTimer()
        self.timer.setInterval(10000)  
        self.timer.timeout.connect(self.on_load_data)
        self.timer.start()

    def on_load_data(self):
        self.status_bar.showMessage("Загрузка данных...")
        self.load_thread = DataLoadThread()
        self.load_thread.data_loaded.connect(self.on_data_loaded)
        self.load_thread.start()

    def on_data_loaded(self, posts):
        if posts:
            self.status_bar.showMessage("Сохранение данных в базу...")
            self.save_thread = DataSaveThread(posts)
            self.save_thread.data_saved.connect(self.on_data_saved)
            self.save_thread.start()
        else:
            self.status_bar.showMessage("Ошибка загрузки данных.")

    def on_data_saved(self, posts):
        if posts:
            self.status_bar.showMessage("Данные успешно сохранены.")
            self.update_table(posts)
        else:
            self.status_bar.showMessage("Ошибка сохранения данных.")

    def update_table(self, posts):
        self.table.setRowCount(len(posts))
        for i, p in enumerate(posts):
            self.table.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(p['userId'])))
            self.table.setItem(i, 2, QTableWidgetItem(p['title']))
            self.table.setItem(i, 3, QTableWidgetItem(p['body']))
        self.status_bar.showMessage("Данные обновлены в интерфейсе.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
