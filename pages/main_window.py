from py_ui.main_window import Ui_Form
from PyQt6.QtWidgets import QWidget, QApplication, QInputDialog
from PyQt6.QtGui import QMouseEvent
from database.db import dao
from .menu_item_widget import MenuItem
from .order_item_widget import OrderItem
class MainWindow(QWidget, Ui_Form):
    def __init__(self, user : dict | None):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle("Главное окно")
        self.user = user
        print(self.user)

        if self.user is None or self.user["role_id"] == 2:
            self.admin_panel.deleteLater()
            self.tabWidget.setTabVisible(1, False)
            self.tabWidget.setTabVisible(3, False)
        
        if self.user is None:
            self.tabWidget.setTabVisible(2, False)
        
        self.load_menu()

    def load_menu(self):
        menu_items = dao.get_menu()
        for mi in menu_items:
            print(f"{mi=}")
            menu_card = MenuItem(mi)
            if self.user is not None and self.user["role_id"] == 2:
                menu_card.double_clicked.connect(self.add_item_to_order)
            self.scroll_layout.addWidget(menu_card)
    
    def add_item_to_order(self, product):
        value, ok = QInputDialog.getInt(self, "Ввод количества блюда", "Количество", 1, 1, 10, 1)

        if ok:
            order_item = OrderItem(product, value)
            self.order_layout.addWidget(order_item)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
        