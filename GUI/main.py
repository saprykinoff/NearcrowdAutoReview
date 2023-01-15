import threading
import time

from PyQt5 import QtWidgets, QtCore, QtGui
from ui_elements.main_ui import Ui_MainWindow
from ui_elements.new_ent_dialog import Ui_NewEnt
from ui_elements.delete_item import Ui_DeleteItem
from ui_elements.verif import Ui_Verif
import open_workplace as owp
import sys
import funcs
import config
from styleSheets import get_style


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.setWindowIcon(icon)
        self.ui.setupUi(self)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.ui.tableWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setWindowTitle(f"NEAR Manager v{config.version}")
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.setStyleSheet(get_style("window"))
        self.make_table()

    # open_browser = QtCore.pyqtSignal(str, str)
    new_acc = QtCore.pyqtSignal()
    new_task = QtCore.pyqtSignal()

    def open_browser(self, acc, task):
        print(f"want to open {acc}, {task}")
        threading.Thread(target=owp.open, args=(acc, task)).start()
        # TODO добавить логировани в консоль

    def make_table(self):
        # TODO сделать стили в табличку
        keys = funcs.get_json("keys", True)
        ftasks = funcs.get_json("tasks", True)
        accounts = list(keys.keys())
        tasks = list(ftasks.keys())
        n = len(accounts) + 1
        m = len(tasks) + 1
        self.ui.tableWidget.setRowCount(n + 1)
        self.ui.tableWidget.setColumnCount(m + 1)
        new_task = QtWidgets.QPushButton(text="New Task")
        new_task.clicked.connect(lambda: self.new_task.emit())
        new_task.setObjectName("new_task")

        self.ui.tableWidget.setCellWidget(0, m, new_task)
        new_account = QtWidgets.QPushButton(text="New Account")
        new_account.setObjectName("new_account")
        new_account.clicked.connect(lambda: self.new_acc.emit())
        self.ui.tableWidget.setCellWidget(n, 0, new_account)
        zz = QtWidgets.QLabel("Account name")
        zz.setObjectName("00")
        self.ui.tableWidget.setCellWidget(0, 0, zz)
        self.ui.tableWidget.setCellWidget(n, m, QtWidgets.QLabel(""))

        for i in range(1, n):
            txt = QtWidgets.QLabel(accounts[i - 1])
            txt.setObjectName("item")
            self.ui.tableWidget.setCellWidget(i, 0, txt)
            self.ui.tableWidget.setCellWidget(i, m, QtWidgets.QLabel(""))
        for j in range(1, m):
            txt = QtWidgets.QLabel(tasks[j - 1])
            txt.setObjectName("item")
            txt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setCellWidget(0, j, txt)
            self.ui.tableWidget.setCellWidget(n, j, QtWidgets.QLabel(""))
        for i in range(1, n):
            for j in range(1, m):
                btn = QtWidgets.QPushButton(text=f"{accounts[i - 1][:2]}/ {ftasks[tasks[j - 1]]}")
                tmp = lambda _, a=accounts[i - 1], b=ftasks[tasks[j - 1]]: self.open_browser(a, b)
                btn.clicked.connect(tmp)
                self.ui.tableWidget.setCellWidget(i, j, btn)

    def add_new_acc(self, short, full, key):
        accounts = funcs.get_json("keys", True)
        accounts[short] = [full, key]
        funcs.update_json("keys", accounts, True)
        self.make_table()
        print(f"New acc: {short}, {full}, {key}")

    def add_new_task(self, short, id):
        tasks = funcs.get_json("tasks", True)
        tasks[short] = id
        funcs.update_json("tasks", tasks, True)
        self.make_table()
        print(f"New task: {short}, {id}")

    def delete_task(self, short):
        tasks = funcs.get_json("tasks", True)
        tasks.pop(short)
        funcs.update_json("tasks", tasks, True)

    def delete_acc(self, short):
        accounts = funcs.get_json("keys", True)
        accounts.pop(short)
        funcs.update_json("keys", accounts, True)


class new_acc_wind(QtWidgets.QDialog):
    accepted = QtCore.pyqtSignal()
    rejected = QtCore.pyqtSignal()
    new_acc = QtCore.pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_NewEnt()
        self.ui.setupUi(self)
        self.setWindowIcon(icon)
        self.setWindowTitle("New Account")
        self.setFixedSize(400, 200)
        self.ui.label.setText("Short name")
        self.ui.label_2.setText("Info message")
        self.ui.lineEdit.setPlaceholderText("Any text")
        self.ui.lineEdit_2.setPlaceholderText("{\"near-api-js:keystore:...")
        self.ui.pushButton.clicked.connect(lambda: self.accepted.emit())
        self.ui.pushButton_2.clicked.connect(lambda: self.rejected.emit())
        self.rejected.connect(self.myreject)
        self.accepted.connect(self.myaccept)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def myaccept(self) -> None:
        short = self.ui.lineEdit.text()
        msg = self.ui.lineEdit_2.text()
        if (msg == "" or short == ""):
            self.ui.errors.setText("All inputs must be non empty")
            return
        accounts = funcs.get_json('keys', True).keys()
        if (short in accounts):
            self.ui.errors.setText("This shortname already used")
            return

        try:
            full = msg.split(":")[2]
            key = msg.split("\"")[3]
            print("accepted")
            self.new_acc.emit(short, full, key)
        except:
            self.ui.errors.setText("Cant parse info message")
            return
        self.close()

    def myreject(self) -> None:
        print("rejected")
        self.close()


class new_task_wind(QtWidgets.QDialog):
    accepted = QtCore.pyqtSignal()
    rejected = QtCore.pyqtSignal()
    new_task = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_NewEnt()
        self.ui.setupUi(self)
        self.setWindowIcon(icon)
        self.setWindowTitle("New Task")
        self.setFixedSize(400, 200)
        self.ui.label.setText("Short name")
        self.ui.label_2.setText("Task_id")
        self.ui.lineEdit.setPlaceholderText("Any text")
        self.ui.lineEdit_2.setPlaceholderText("-1")
        self.ui.pushButton.clicked.connect(lambda: self.accepted.emit())
        self.ui.pushButton_2.clicked.connect(lambda: self.rejected.emit())
        self.rejected.connect(self.myreject)
        self.accepted.connect(self.myaccept)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def myaccept(self) -> None:
        short = self.ui.lineEdit.text()
        id = self.ui.lineEdit_2.text()
        if (id == "" or short == ""):
            self.ui.errors.setText("All inputs must be non empty")
            return
        tasks = funcs.get_json('tasks', True).keys()
        if (short in tasks):
            self.ui.errors.setText("This shortname already used")
            return
        self.new_task.emit(short, id)
        self.close()

    def myreject(self) -> None:
        print("rejected")
        self.close()


class delete_item_wind(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DeleteItem()
        self.ui.setupUi(self)
        self.setWindowIcon(icon)
        self.setFixedSize(400, 200)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.cancel.clicked.connect(lambda: self.close())


class verification_wind(QtWidgets.QMainWindow):
    def __init__(self, rem):
        super().__init__()
        self.ui = Ui_Verif()
        self.ui.setupUi(self)
        self.setWindowIcon(icon)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(600, 200)
        self.ui.label.setObjectName("heading")
        self.ui.textBrowser.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.ok = True

        if (rem >= config.safe_time):
            self.ui.label.setText("Verification Success")
            self.ui.textBrowser.setText(f"Your license was verified. Remains: {funcs.secs_to_remain(rem)}")
        elif (rem > 0):
            self.ui.label.setText("Verification Warning")
            self.ui.textBrowser.setText(
                f"Remains: {funcs.secs_to_remain(rem)}. Please be ready to program closure and save your work")
        elif (rem == 0):
            self.ok = False
            self.ui.label.setText("Verification Error")
            self.ui.textBrowser.setText(
                f"Your license has expired. See details here: https://t.me/nearmgr. Your id: {funcs.get_cpuid()}")
        else:
            self.ok = False
            self.ui.label.setText("Verification Error")
            self.ui.textBrowser.setText(
                f"Server connection error. Channel of the project: https://t.me/nearmgr. Your id: {funcs.get_cpuid()}")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("verif_wind closed")
        if (not self.ok):
            sys.exit(0)


class Checker(QtCore.QThread):
    def __init__(self):
        super(Checker, self).__init__()

    tick = QtCore.pyqtSignal()

    def run(self) -> None:
        while 1:
            self.tick.emit()
            time.sleep(10)


class Controller:
    def __init__(self):
        self.id = funcs.get_cpuid()

    first_time = True
    notified = False
    finished = False

    def start(self):
        self.thread = Checker()
        self.thread.tick.connect(self.work)
        self.thread.start()
        self.application = mainwindow()
        self.application.new_acc.connect(self.create_new_acc)
        self.application.new_task.connect(self.create_new_task)
        self.application.ui.tableWidget.cellClicked.connect(self.delete_item)
        self.application.show()
        print("showed")

    def work(self):
        if (self.finished):
            return
        print("aga")
        rem = funcs.ask_remain_time(self.id)
        print("checked")
        if (rem <= 0):
            self.verif = verification_wind(rem)
            self.verif.show()
            self.finished = True

        if (rem >= config.safe_time and self.first_time):
            self.verif = verification_wind(rem)
            self.verif.show()
            self.first_time = False
        if (rem < config.safe_time and not self.notified):
            self.verif = verification_wind(rem)
            self.verif.show()
            self.notified = True

    def create_new_acc(self):
        new_wind = new_acc_wind()
        new_wind.new_acc.connect(self.application.add_new_acc)
        new_wind.show()
        print(f"want to new acc")

    def create_new_task(self):
        new_wind = new_task_wind()
        new_wind.new_task.connect(self.application.add_new_task)
        new_wind.show()
        print(f"want to new task")

    def delete_item(self, i, j):
        if (i * j != 0 or i + j == 0):
            return
        new_wind = delete_item_wind()
        name = ""
        if (j == 0):
            accounts = list(funcs.get_json("keys", True).keys())
            name = accounts[i - 1]
            new_wind.ui.label.setText(f"Are you sure you want to delete account {name}?")
            new_wind.ui.ok.clicked.connect(lambda x=name: delete_acc(name))
            new_wind.setWindowTitle("Delete Account")
        else:
            tasks = list(funcs.get_json("tasks", True).keys())
            name = tasks[j - 1]
            new_wind.ui.label.setText(f"Are you sure you want to delete task {name}?")
            new_wind.ui.ok.clicked.connect(lambda x=name: delete_task(name))
            new_wind.setWindowTitle("Delete Task")

        new_wind.show()

        def delete_task(name):
            self.application.delete_task(name)
            new_wind.close()
            self.application.make_table()

        def delete_acc(name):
            self.application.delete_acc(name)
            new_wind.close()
            self.application.make_table()


app = QtWidgets.QApplication([])
icon = QtGui.QIcon(funcs.resource_path("images/logo.ico"))
app.setStyleSheet(get_style("main"))
controller = Controller()
controller.start()
sys.exit(app.exec())
