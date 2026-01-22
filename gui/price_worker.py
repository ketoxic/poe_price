from PyQt5.QtCore import QThread, pyqtSignal
import time

from core.price_runner import run_price_check


class PriceWorker(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, item_file):
        super().__init__()
        self.item_file = item_file
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        try:
            # inject hook để log + check stop
            def log_hook(msg: str):
                self.log.emit(msg)

            def should_stop():
                return not self._running

            run_price_check(
                self.item_file,
                log_hook=log_hook,
                should_stop=should_stop
            )

        except Exception as e:
            self.error.emit(str(e))

        self.finished.emit()
