from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QStringListModel
from pathlib import Path
import json
from typing import Optional
from core.price_runner import run_price_check


class PriceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi("gui/price_check.ui", self)

        # model cho list view
        self.item_model = QStringListModel()
        self.list_item.setModel(self.item_model)

        # signals
        self.select_file_item.clicked.connect(self.choose_item_file)
        self.check_price_button.clicked.connect(self.start_price_check)

        self.item_file: Optional[Path] = None

    # --------------------------------------------------
    # chọn file json
    # --------------------------------------------------
    def choose_item_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select item json",
            "",
            "JSON Files (*.json)"
        )

        if not path:
            return

        self.item_file = Path(path)
        self.item_path.setText(path)
        self.load_item_list()

    # --------------------------------------------------
    # load item từ json → list view
    # --------------------------------------------------
    def load_item_list(self):
        try:
            with open(self.item_file, "r", encoding="utf-8") as f:
                items = json.load(f)

            self.item_model.setStringList(items)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", f"Failed to load json:\n{e}"
            )

    # --------------------------------------------------
    # chạy price check
    # --------------------------------------------------
    def start_price_check(self):
        if not self.item_file:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Please select item json first"
            )
            return

        self.check_price_button.setEnabled(False)
        self.check_price_button.setText("Running...")

        try:
            run_price_check(self.item_file)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error", str(e)
            )

        self.check_price_button.setEnabled(True)
        self.check_price_button.setText("Check Price")
