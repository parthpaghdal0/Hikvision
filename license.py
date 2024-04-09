
from license_ui import Ui_License
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSlot

from cryptography import generate_license

class Widget(QWidget, Ui_License):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pb_generate_clicked(self):
        license = generate_license(self.le_ip.text())
        self.te_license.setPlainText(license)