from PyQt6.QtWidgets import QApplication
from pages.auth_window import AuthWindow
if __name__ == '__main__':
    app = QApplication([])
    window = AuthWindow()
    window.show()
    app.exec()
