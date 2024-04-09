
import os
import sys
import winreg

from PyQt6.QtWidgets import QApplication

from widget import Widget

def add_to_startup(file_path):
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
        winreg.SetValueEx(reg_key, "hikvisionCRM", 0, winreg.REG_SZ, file_path)

if __name__ == "__main__":
    script_path = sys.argv[0]
    exe_name = os.path.basename(script_path)
    script_dir = os.path.dirname(sys.argv[0])
    exe_path = os.path.join(script_dir, exe_name)
    add_to_startup(exe_path)

    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())
