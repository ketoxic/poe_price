import sys
from PyQt5.QtWidgets import QApplication
from gui.price_window import PriceWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PriceWindow()
    win.show()
    sys.exit(app.exec_())
