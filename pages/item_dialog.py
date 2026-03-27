from py_ui.item_dialog import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QFileDialog
from database.db import dao


class ItemDialog(QDialog, Ui_Dialog):
    def __init__(self, menu_item: dict | None = None):
        super().__init__()
        self.setupUi(self)
        self.menu_item = menu_item
        self.uploadImageButton.clicked.connect(self.handle_upload)
        self.load_categories()
        self.applyButton.clicked.connect(self.accept)

        self.set_data()

    def set_data(self):
        if self.menu_item is not None:
            self.nameLineEdit.setText(self.menu_item["name"])
            self.descriptionLineEdit.setText(self.menu_item["description"])
            self.priceDoubleSpinBox.setValue(self.menu_item["price"])
            self.imageLineEdit.setText(self.menu_item["image"])
            self.categoryComboBox.setCurrentIndex(
                self.categoryComboBox.findText(self.menu_item["category"])
            )

    def load_categories(self):
        categories = dao.get_categories()
        for category in categories:
            self.categoryComboBox.addItem(category["category"])

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбор изображения", None, "Изображения (*.png, *.jpeg, *.jpg)"
        )
        self.imageLineEdit.setText(file_path)

    def get_data(self):
        name = self.nameLineEdit.text()
        composition = self.descriptionLineEdit.text()
        price = self.priceDoubleSpinBox.value()
        category = self.categoryComboBox.currentText()
        image_path = self.imageLineEdit.text()
        return (name, composition, price, category, image_path)
