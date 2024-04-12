

import os
import keyboard
import pyodbc
from datetime import datetime

from widget_ui import Ui_Widget
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QSettings, QTimer, pyqtSlot, pyqtSignal

from cryptography import validate_license
from camera import Camera

program_data_dir = os.getenv('ProgramData')
ini_file_path = os.path.join(program_data_dir, 'hikvisionCRM', 'settings.ini')

class Widget(QWidget, Ui_Widget):
    hotkeySignal = pyqtSignal()
    hotkey = ''
    timer = QTimer()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.l_settings_hotkey.hide()
        self.pb_settings_hotkey.hide()
        self.camera.hide()
        self.odbc.hide()
        self.l_settings_companyid.hide()
        self.le_settings_companyid.hide()
        self.l_settings_delay.hide()
        self.le_settings_delay.hide()
        self.l_settings_license.hide()
        self.te_settings_license.hide()

        self.resize(240, 120)

        self.hotkeySignal.connect(self.on_hotkey_slot)

        timer = QTimer()

    def showEvent(self, event):
        settings = QSettings(ini_file_path, QSettings.Format.IniFormat)

        settings.beginGroup("camera")
        self.le_camera_ip.setText(settings.value("ip"))
        self.le_camera_username.setText(settings.value("username"))
        self.le_camera_password.setText(settings.value("password"))
        settings.endGroup()

        settings.beginGroup("odbc")
        self.le_odbc_ip.setText(settings.value("ip"))
        self.le_odbc_username.setText(settings.value("username"))
        self.le_odbc_password.setText(settings.value("password"))
        settings.endGroup()

        settings.beginGroup("settings")
        self.le_settings_userid.setText(settings.value("userid", "S5NICK"))
        self.le_settings_companyid.setText(settings.value("companyid"))
        self.le_settings_delay.setText(settings.value("delay", "5"))
        self.hotkey = settings.value("hotkey", "Ctrl+Shift+Q")
        self.l_settings_hotkey.setText(settings.value("hotkey", "Ctrl+Shift+Q"))
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
        if self.le_odbc_ip.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input ODBC ip address.')
            return
        if self.le_odbc_username.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input ODBC username.')
            return
        if self.le_odbc_password.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input ODBC password.')
            return
        if self.le_settings_userid.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input user id.')
            return
        if self.le_settings_companyid.text() == "":
            QMessageBox.warning(self, 'Warning', 'Please input company id.')
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

        settings.beginGroup("odbc")
        settings.setValue("ip", self.le_odbc_ip.text())
        settings.setValue("username", self.le_odbc_username.text())
        settings.setValue("password", self.le_odbc_password.text())
        settings.endGroup()

        settings.beginGroup("camera")
        settings.setValue("ip", self.le_camera_ip.text())
        settings.setValue("username", self.le_camera_username.text())
        settings.setValue("password", self.le_camera_password.text())
        settings.endGroup()

        settings.beginGroup("settings")
        settings.setValue("userid", self.le_settings_userid.text().upper())
        settings.setValue("companyid", self.le_settings_companyid.text())
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

    @pyqtSlot()
    def on_pb_odbc_test_clicked(self):
        ip = self.le_odbc_ip.text()
        username = self.le_odbc_username.text()
        password = self.le_odbc_password.text()
        try:
            url = 'DRIVER={iSeries Access ODBC Driver};SYSTEM=%s;DATABASE=IWSE4S5;UID=%s;PWD=%s' % (ip, username, password)
            pyodbc.connect(url)
            QMessageBox.information(self, 'Information', 'Connection was successful.')
        except:
            QMessageBox.warning(self, 'Warning', 'Connection was unsuccessful.')

    def on_hotkey_pressed(self, event):
        if keyboard.is_pressed(self.hotkey):
            self.hotkeySignal.emit()

    def parseResult(self, row):
        result = '%s-%s, %s, %s, %s, %s, %s' % (row[0], row[1], str(row[2]).strip(), str(row[3]).strip(), row[4], row[5], str(row[6]).strip())
        return result
    
    @pyqtSlot()
    def on_timeout(self):
        ip = self.le_camera_ip.text()
        username = self.le_camera_username.text()
        password = self.le_camera_password.text()

        Camera.clearTextOverlay(ip, username, password)
        print("Clean was successful")

    @pyqtSlot()
    def on_hotkey_slot(self):
        ip = self.le_odbc_ip.text()
        username = self.le_odbc_username.text()
        password = self.le_odbc_password.text()
        print("Running Hotkey...")
        try:
            url = 'DRIVER={iSeries Access ODBC Driver};SYSTEM=%s;DATABASE=IWSE4S5;UID=%s;PWD=%s' % (ip, username, password)
            conn = pyodbc.connect(url)
            cursor = conn.cursor()

            cursor.execute('SELECT STCOMP, Max(STTCKT) AS MaxOfSTTCKT, STUSER\
                FROM Iwse4s5.SCTRN\
                GROUP BY STCOMP, STUSER, STDATE\
                HAVING ((STUSER=?) AND (STDATE=?))', self.le_settings_userid.text(), datetime.today().strftime('%Y%m%d')) #datetime.today().strftime('%Y%m%d')
            rows = cursor.fetchall()
            STTTCKT = rows[0][1]
            print("Ticket Number is = " + str(STTTCKT))

            cursor.execute('SELECT stcomp, sttckt, stdesc, cblnam, STGROS AS Gross, STTARE AS Tare, STVEH1\
                FROM Iwse4s5.CUST INNER JOIN Iwse4s5.SCTRN ON (Iwse4s5.CUST.CCUST# = Iwse4s5.SCTRN.STCUST) AND (Iwse4s5.CUST.CCMPNY = Iwse4s5.SCTRN.STCOMP)\
                WHERE (((Iwse4s5.SCTRN.STCOMP)=?) AND ((Iwse4s5.SCTRN.STTCKT)=?))', self.le_settings_companyid.text(), STTTCKT)
            rows = cursor.fetchall()
            text1 = self.parseResult(rows[0])
            text2 = self.parseResult(rows[1])

            ip = self.le_camera_ip.text()
            username = self.le_camera_username.text()
            password = self.le_camera_password.text()
            if Camera.writeTextOverlay(ip, username, password, text1, text2) == True:
                print("Write was successful")
            else:
                print("Write failed")

            cursor.close()
            conn.close()

            delay = int(self.le_settings_delay.text()) * 1000
            self.timer.singleShot(delay, self.on_timeout)
        except Exception as e:
            print("Failed to run hotkey.", e)