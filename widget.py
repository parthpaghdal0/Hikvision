

import os
import keyboard

from widget_ui import Ui_Widget
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSettings, pyqtSlot, pyqtSignal

from cryptography import validate_license
from camera import Camera

program_data_dir = os.getenv('ProgramData')
ini_file_path = os.path.join(program_data_dir, 'hikvisionCRM', 'settings.ini')

class Widget(QWidget, Ui_Widget):
    hotkeySignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.l_settings_hotkey.hide()
        self.pb_settings_hotkey.hide()

        self.hotkeySignal.connect(self.on_hotkey_slot)

    def showEvent(self, event):
        settings = QSettings(ini_file_path, QSettings.Format.IniFormat)

        settings.beginGroup("camera")
        self.le_camera_ip.setText(settings.value("ip"))
        self.le_camera_username.setText(settings.value("username"))
        self.le_camera_password.setText(settings.value("password"))
        settings.endGroup()

        settings.beginGroup("settings")
        self.le_settings_userid.setText(settings.value("userid", "S5NICK"))
        self.le_settings_delay.setText(settings.value("delay", "5"))
        self.l_settings_hotkey.setText(settings.value("hotkey", "Ctrl+Shift+P"))
        self.te_settings_license.setPlainText(settings.value("license"))
        settings.endGroup()

        keyboard.on_press(self.on_hotkey_pressed)

    @pyqtSlot()
    def on_pb_start_clicked(self):
        settings = QSettings(ini_file_path, QSettings.Format.IniFormat)

        if self.le_camera_ip.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input camera ip address.')
            return
        if self.le_camera_username.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input camera username.')
            return
        if self.le_camera_password.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input camera password.')
            return
        if self.le_settings_userid.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input user id.')
            return
        if self.le_settings_delay.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input delay.')
            return
        if self.te_settings_license.toPlainText() == "":
            QMessageBox.warning(self, 'Warning', 'Please input license.')
            return
        if validate_license(self.le_camera_ip.text(), self.te_settings_license.toPlainText()) == False:
            QMessageBox.warning(self, 'Warning', 'Your license is invalid.')
            return

        settings.beginGroup("camera")
        settings.setValue("ip", self.le_camera_ip.text())
        settings.setValue("username", self.le_camera_username.text())
        settings.setValue("password", self.le_camera_password.text())
        settings.endGroup()

        settings.beginGroup("settings")
        settings.setValue("userid", self.le_settings_userid.text().upper())
        settings.setValue("delay", self.le_settings_delay.text())
        settings.setValue("hotkey", self.l_settings_hotkey.text())
        settings.setValue("license", self.te_settings_license.toPlainText())
        settings.endGroup()

        self.hide()

    @pyqtSlot()
    def on_pb_camera_test_clicked(self):
        ip = self.le_camera_ip.text()
        username = self.le_camera_username.text()
        password = self.le_camera_password.text()
        if Camera.test(ip, username, password) == True:
            QMessageBox.information(self, 'Information', 'Connection was successful.')
        else:
            QMessageBox.warning(self, 'Warning', 'Connection was unsuccessful.')

    def on_hotkey_pressed(self, event):
        if keyboard.is_pressed('CTRL+SHIFT+Q'):
            self.hotkeySignal.emit()

    @pyqtSlot()
    def on_hotkey_slot(self):
        print('hotkey pressed')
        pass