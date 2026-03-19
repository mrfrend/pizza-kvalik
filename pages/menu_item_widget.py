from py_ui.menu_item_widget import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtCore import pyqtSignal
from database.db import dao

class MenuItem(QWidget, Ui_Form):
    double_clicked = pyqtSignal(dict)

    def __init__(self, product):
        super().__init__()
        self.setupUi(self)
        self.product = product
        print(f"{self.product=}")
        
        text = self.product["name"]
        image_path = "Pizza/" + self.product['image']

        pixmap = QPixmap(image_path).scaled(100, 100)
        self.image.setPixmap(pixmap)

        self.text.setText(text)
    
    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        self.double_clicked.emit(self.product)
