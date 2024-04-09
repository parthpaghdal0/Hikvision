
import os
from PyQt6.QtCore import QSettings

program_data_dir = os.getenv('ProgramData')
ini_file_path = os.path.join(program_data_dir, 'hikvisionCRM', 'settings.ini')

class Settings:
    @staticmethod
    def addUser(data):
        settings = QSettings(ini_file_path, QSettings.Format.IniFormat)

        count = int(settings.value("users", 0))
        group = "user" + str(count)

        settings.beginGroup(group)
        settings.setValue("username", data.username)
        settings.setValue("password", data.password)
        settings.setValue("proxy", data.proxy)
        settings.endGroup()

        settings.setValue("users", count + 1)

    @staticmethod
    def editUser(index, data):
        settings = QSettings("users.ini", QSettings.Format.IniFormat)

        group = "user" + str(index)

        settings.beginGroup(group)
        settings.setValue("username", data.username)
        settings.setValue("password", data.password)
        settings.setValue("proxy", data.proxy)
        settings.endGroup()

    @staticmethod
    def deleteUser(index):
        list = Settings.getUsers()
        del list[index]

        settings = QSettings("users.ini", QSettings.Format.IniFormat)
        settings.clear()

        count = len(list)
        for i in range(count):
            group = "user" + str(i)
            data = list[i]

            settings.beginGroup(group)

            settings.setValue("username", data.username)
            settings.setValue("password", data.password)
            settings.setValue("proxy", data.proxy)
            settings.endGroup()

        settings.setValue("users", count)

    @staticmethod
    def getUsers():
        list = []
        settings = QSettings("users.ini", QSettings.Format.IniFormat)

        count = int(settings.value("users", 0))
        for i in range(count):
            group = "user" + str(i)

            settings.beginGroup(group)

            username = settings.value("username")
            password = settings.value("password")
            proxy = settings.value("proxy")
            list.append(UserData(username, password, proxy))
            settings.endGroup()

        return list

    @staticmethod
    def getUser(index):
        settings = QSettings("users.ini", QSettings.Format.IniFormat)

        group = "user" + str(index)

        settings.beginGroup(group)

        username = settings.value("username")
        password = settings.value("password")
        proxy = settings.value("proxy")
        settings.endGroup()

        return UserData(username, password, proxy)
