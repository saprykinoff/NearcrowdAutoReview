import threading

import config
import os
import json
import wmi
import requests
from PyQt5 import QtWidgets, QtGui
from ui_elements.error_window import Ui_ErrorWindow
from ui_elements.info_window import Ui_InfoWindow
from styleSheets import get_style
import sys


def get_json(name, user):
    if (user == True):
        pathi = config.user_workdir
    else:
        pathi = config.app_workdir
    path = os.path.join(pathi, f"{name}.json")
    if (not os.path.exists(path)):
        with open(path, "w"):
            pass
    if os.stat(path).st_size == 0:
        return dict()
    with open(path, "r") as f:
        return json.load(f)


def update_json(name, val, user):
    if (user == True):
        pathi = config.user_workdir
    else:
        pathi = config.app_workdir
    path = os.path.join(pathi, f"{name}.json")
    with open(path, "w") as f:
        json.dump(val, f, indent=4)


class InfoWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(InfoWindow, self).__init__()
        self.ui = Ui_InfoWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path('images/logo.ico')))
        self.setFixedSize(600, 200)


class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ErrorWindow, self).__init__()
        self.ui = Ui_ErrorWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path('images/logo.ico')))
        self.setFixedSize(600, 200)


def message(msg, type):
    app = QtWidgets.QApplication([])
    app.setStyleSheet(get_style("popups"))
    w1 = None
    if (type == "error"):
        w1 = ErrorWindow()
    if (type == "info"):
        w1 = InfoWindow()

    w1.ui.label.setText(msg)
    w1.show()
    app.exec()


def error(msg):
    threading.Thread(target=message, args=(msg, "error")).start()


def info(msg):
    threading.Thread(target=message, args=(msg, "info")).start()


def get_cpuid():
    for comp in wmi.WMI().Win32_Processor():
        for s in str(comp).split("\n"):
            s = str(s).replace(';', '').strip().split(" = ")
            # s = str(s).split(" = ")
            # print(s)
            if (s[0] == "ProcessorId"):
                return s[1].replace('"', '')
    return "ERROR"


def secs_to_remain(secs):
    s = secs % 60
    m = secs // 60
    h = m // 60
    m %= 60
    days = h // 24
    h %= 24
    return f"{days} days {h} hours {m} minutes {s} seconds"


def ask_remain_time(cpuid):
    try:
        url = f"http://{config.verification_link}/remain.php?id={cpuid}"
        print(url)
        date = requests.get(url).content
        return int(date)
    except requests.ConnectTimeout:
        return 0


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
