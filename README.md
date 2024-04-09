### To build ui into py

pyuic6 -o widget_ui.py ui/widget.ui
pyuic6 -o license_ui.py ui/license.ui

### To build python into exe

pyinstaller --onefile --windowed main.py
pyinstaller --onefile --windowed licenseapp.py
