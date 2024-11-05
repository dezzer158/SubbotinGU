import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QDialog, QLabel, QFormLayout, QSpinBox, QLineEdit, QTextEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                body TEXT
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()


class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")

        self.user_id_input = QSpinBox()
        self.title_input = QLineEdit()
        self.body_input = QTextEdit()

        form_layout = QFormLayout()
        form_layout.addRow("User ID:", self.user_id_input)
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Body:", self.body_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_data(self):
        return self.user_id_input.value(), self.title_input.text(), self.body_input.toPlainText()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI с базой данных")
        self.resize(800, 600)

        self.db_manager = DatabaseManager()
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database.db")
        self.db.open()

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Модель для таблицы
        self.model = QSqlTableModel(self)
        self.model.setTable("records")
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "User ID")
        self.model.setHeaderData(2, Qt.Horizontal, "Title")
        self.model.setHeaderData(3, Qt.Horizontal, "Body")

        # Прокси-модель для фильтрации
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(2)  # Фильтр по полю "Title"

        # Таблица
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)

        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по заголовку")
        self.search_input.textChanged.connect(self.on_search)

        # Кнопки
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.refresh_data)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_record)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_record)

        # Размещение элементов
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)

        main_widget.setLayout(layout)

    def refresh_data(self):
        self.model.select()

    def on_search(self, text):
        self.proxy_model.setFilterFixedString(text)

    def add_record(self):
        dialog = AddRecordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            user_id, title, body = dialog.get_data()
            query = QSqlTableModel.query(self.model)
            query.prepare("INSERT INTO records (user_id, title, body) VALUES (?, ?, ?)")
            query.addBindValue(user_id)
            query.addBindValue(title)
            query.addBindValue(body)
            if query.exec_():
                self.model.select()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить запись")

    def delete_record(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if selected_indexes:
            confirm = QMessageBox.question(self, "Подтверждение", "Удалить выбранную запись?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                index = selected_indexes[0]
                record_id = self.model.data(self.model.index(index.row(), 0))
                query = QSqlTableModel.query(self.model)
                query.prepare("DELETE FROM records WHERE id = ?")
                query.addBindValue(record_id)
                if query.exec_():
                    self.model.select()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")

    def closeEvent(self, event):
        self.db.close()
        self.db_manager.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
