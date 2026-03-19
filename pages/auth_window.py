from PyQt6.QtCore import Qt

from py_ui.auth import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from database.db import dao
from pages.main_window import MainWindow

class AuthWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_window = None
        self.user = None
        self.loginButton.clicked.connect(self.auth)
        self.gostButton.clicked.connect(self.open_main_window)

    def auth(self):
        login = self.loginEdit.text().strip()
        password = self.passwordEdit.text().strip()

        self.user = dao.authorize(login, password)

        if self.user is None:
            QMessageBox.critical(self, "Ошибка авторизации", "Неправильный логин или пароль")
            return

        QMessageBox.information(self, "Успех", "Вы авторизованы!")

        self.open_main_window()
    
    def open_main_window(self):
        self.main_window = MainWindow(self.user)
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = AuthWindow()
    window.show()
    app.exec()
        
