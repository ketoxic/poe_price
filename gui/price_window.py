from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QStringListModel
from pathlib import Path
import json
from typing import Optional


class PriceWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi("gui/price_check.ui", self)

        # model cho list view
        self.item_model = QStringListModel()
        self.list_item.setModel(self.item_model)

        # cho phép chọn nhiều item
        self.list_item.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        # signals
        self.select_file_item.clicked.connect(self.choose_item_file)
        self.check_price_button.clicked.connect(self.start_price_check)

        # optional cancel button (nếu có trong UI)
        if hasattr(self, "cancel_button"):
            self.cancel_button.clicked.connect(self.stop_worker)

        self.item_file: Optional[Path] = None
        self.worker = None

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
    # lấy item được chọn
    # --------------------------------------------------
    def get_selected_items(self):
        indexes = self.list_item.selectedIndexes()
        return [index.data() for index in indexes]

    # --------------------------------------------------
    # chạy price check
    # --------------------------------------------------
    def start_price_check(self):
        if not self.item_file:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Please select item json first"
            )
            return

        selected_items = self.get_selected_items()

        if not selected_items:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Please select at least 1 item"
            )
            return

        self.check_price_button.setEnabled(False)
        self.check_price_button.setText("Running...")

        from gui.price_worker import PriceWorker

        self.worker = PriceWorker(selected_items)

        self.worker.log.connect(self.append_log)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.finished.connect(self.worker.deleteLater)

        self.worker.start()

    # --------------------------------------------------
    # stop worker
    # --------------------------------------------------
    def stop_worker(self):
        if self.worker:
            self.worker.stop()

    # --------------------------------------------------
    # handlers
    # --------------------------------------------------
    def on_finished(self):
        self.check_price_button.setEnabled(True)
        self.check_price_button.setText("Check Price")

    def on_error(self, msg):
        QtWidgets.QMessageBox.critical(self, "Error", msg)

    def append_log(self, msg):
        if hasattr(self, "log_box"):
            self.log_box.append(msg)
        else:
            print(msg)