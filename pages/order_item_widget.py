from py_ui.order_item_widget import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal

class OrderItem(QWidget, Ui_Form):
    def __init__(self, product, count):
        super().__init__()
        self.setupUi(self)
        self.product = product
        self.count = count

         
        text = self.product["name"]
        image_path = "Pizza/" + self.product['image']

        pixmap = QPixmap(image_path).scaled(100, 100)
        self.image.setPixmap(pixmap)
        self.item_name.setText(text)
        self.amountBox.setValue(count)
        self.price_label.setText(str(self.product['price']))
