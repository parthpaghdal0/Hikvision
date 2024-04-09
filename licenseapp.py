
import sys

from PyQt6.QtWidgets import QApplication

from license import Widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())
