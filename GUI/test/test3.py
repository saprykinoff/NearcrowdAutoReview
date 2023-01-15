import sys
from PyQt5 import QtWidgets
from ui_elements.new_ent_dialog import Ui_NewEnt
class mydialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NewEnt()
        self.ui.setupUi(self)


app = QtWidgets.QApplication([])
my = mydialog()
my.show()


sys.exit(app.exec())