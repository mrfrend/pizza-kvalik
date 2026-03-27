from py_ui.main_window import Ui_Form
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QInputDialog,
    QMessageBox,
    QDialog,
    QTableWidgetItem,
    QComboBox,
)
from PyQt6.QtGui import QMouseEvent
import pymysql
from pages.order_order_item import OrderOrderItem
from database.db import dao
from .menu_item_widget import MenuItem
from .order_item_widget import OrderItem
from pages.item_dialog import ItemDialog
import shutil


class MainWindow(QWidget, Ui_Form):
    def __init__(self, user: dict | None):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle("Главное окно")
        self.user = user
        self.selected = None
        print(self.user)
        self.order_items: list[MenuItem] = []

        if self.user is None or self.user["role_id"] == 2:
            self.admin_panel.deleteLater()
            self.tabWidget.setTabVisible(1, False)
            self.tabWidget.setTabVisible(3, False)

        if self.user is not None and self.user["role_id"] == 5:
            self.tabWidget.setTabVisible(2, False)

        if self.user is None:
            self.tabWidget.setTabVisible(2, False)

        self.pushButton_2.clicked.connect(self.apply_order)
        self.apply_slots()

        self.load_menu()
        self.load_orders()
        self.load_orders_table()
        self.load_statuses()

    def apply_slots(self):
        if self.user and self.user["role_id"] == 5:
            self.addButton.clicked.connect(self.on_add)
            self.deleteButton.clicked.connect(self.on_delete)
            self.editButton.clicked.connect(self.on_edit)
            self.status_combobox.currentIndexChanged.connect(self.load_orders_table)

    def load_statuses(self):
        if self.user and self.user["role_id"] == 5:
            statuses = dao.get_statuses()
            self.status_combobox.addItem("Все", None)
            for status in statuses:
                self.status_combobox.addItem(status["status"], status["status"])

    def on_add(self):
        item_dialog = ItemDialog()
        if item_dialog.exec() == QDialog.DialogCode.Accepted:
            name, composition, price, category, image_path = item_dialog.get_data()
            image_name = image_path.split("/")[-1]
            dao.insert_menu_item(name, composition, price, category, image_name)
            shutil.copy2(image_path, f"E:/Projects/pizza-kvalik/Pizza/{image_name}")
            self.load_menu()

    def on_delete(self):
        if self.selected is None:
            QMessageBox.warning(
                self, "Ошибка", "Выберите товар при помощи двойного ЛКМ"
            )
            return
        dao.delete_menu_item(self.selected["item_id"])
        self.load_menu()

    def on_edit(self):
        if self.selected is None:
            QMessageBox.warning(
                self, "Ошибка", "Выберите товар при помощи двойного ЛКМ"
            )
            return

        item_dialog = ItemDialog(self.selected)
        if item_dialog.exec() == QDialog.DialogCode.Accepted:
            name, composition, price, category, image_path = item_dialog.get_data()
            image_name = image_path.split("/")[-1]
            dao.update_menu_item(
                self.selected["item_id"], name, composition, price, category, image_name
            )
            if image_path != self.selected["image"]:
                shutil.copy2(image_path, f"E:/Projects/pizza-kvalik/Pizza/{image_name}")
            self.load_menu()

    def apply_order(self):
        try:
            dao.create_order(self.user["user_id"], self.order_items)

            while self.order_layout.count():
                widget = self.order_layout.takeAt(0).widget()
                if widget is not None:
                    widget.deleteLater()
            self.order_items = []

            QMessageBox.information(self, "Успех", "Ваш заказ оформлен!")

        except pymysql.err.Error as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_orders(self):
        if self.user is not None:
            orders = dao.get_orders_of_user(self.user["user_id"])
            for order in orders:
                order_composition = dao.get_order_composition(
                    order["order_id"]
                )  # ({"composition": "Маргарита x 1"})
                order_composition_str = ", ".join(
                    [comp["composition"] for comp in order_composition]
                )
                order_order_item = OrderOrderItem(order, order_composition_str)
                self.orders_layout.addWidget(order_order_item)

    def load_orders_table(self):
        if self.user and self.user["role_id"] == 5:
            status = self.status_combobox.currentData()
            statuses = [status["status"] for status in dao.get_statuses()]
            orders = dao.get_orders(status)
            self.orders_table.clear()
            self.orders_table.verticalHeader().hide()
            self.orders_table.setRowCount(len(orders))
            self.orders_table.setColumnCount(len(orders[0]))

            self.orders_table.setHorizontalHeaderLabels(
                ["ID заказа", "Дата", "Цена", "Статус"]
            )

            for row_idx, row in enumerate(orders):
                self.orders_table.setItem(
                    row_idx, 0, QTableWidgetItem(str(row["order_id"]))
                )
                self.orders_table.setItem(
                    row_idx, 1, QTableWidgetItem(str(row["order_date"]))
                )
                self.orders_table.setItem(
                    row_idx, 2, QTableWidgetItem(str(row["total_amount"]))
                )

                status_combo = QComboBox()
                status_combo.addItems(statuses)
                status_combo.setCurrentIndex(status_combo.findText(row["status"]))
                status_combo.currentTextChanged.connect(
                    lambda status, order_id=row[
                        "order_id"
                    ]: self.on_change_order_status(order_id, status)
                )

                self.orders_table.setCellWidget(row_idx, 3, status_combo)

    def on_change_order_status(self, order_id: int, status: str):
        dao.update_order_status(order_id, status)

    def load_menu(self):
        while self.scroll_layout.count():
            widget = self.scroll_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        menu_items = dao.get_menu()
        for mi in menu_items:
            print(f"{mi=}")
            menu_card = MenuItem(mi)
            if self.user is not None and self.user["role_id"] == 2:
                menu_card.double_clicked.connect(self.add_item_to_order)
            elif self.user is not None and self.user["role_id"] == 5:
                menu_card.double_clicked.connect(self.on_choose_menu_card)
            self.scroll_layout.addWidget(menu_card)

    def on_choose_menu_card(self, product):
        self.selected = product
        QMessageBox.information(self, "Выбор", f"Вы выбрали блюдо {product['name']}")

    def add_item_to_order(self, product):
        value, ok = QInputDialog.getInt(
            self, "Ввод количества блюда", "Количество", 1, 1, 10, 1
        )

        if ok:
            order_item = OrderItem(product, value)
            self.order_layout.addWidget(order_item)
            self.order_items.append(order_item)
            self.pushButton_2.setEnabled(len(self.order_layout) > 0)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
