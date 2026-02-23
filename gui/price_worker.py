from PyQt5.QtCore import QThread, pyqtSignal
from core.price_runner import run_price_check


class PriceWorker(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, items):
        super().__init__()
        self.items = items
        self._running = True

    def stop(self):
        self._running = False
        self.log.emit("Stopping...")

    def run(self):
        try:
            def log_hook(msg: str):
                self.log.emit(msg)

            def should_stop():
                return not self._running

            run_price_check(
                items=self.items,
                log_hook=log_hook,
                should_stop=should_stop
            )

        except Exception as e:
            self.error.emit(str(e))
            return

        self.finished.emit()