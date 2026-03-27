from py_ui.order_order_item import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal


class OrderOrderItem(QWidget, Ui_Form):
    def __init__(self, order, order_composition):
        super().__init__()
        self.setupUi(self)
        self.order = order
        self.order_composition = order_composition
        self.order_id.setText(f"Заказ №{self.order['order_id']}")
        self.composition.setText(order_composition)
        self.price_label.setText(str(self.order["total_amount"]))
        self.status.setText(self.order["status"])
