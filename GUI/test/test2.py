from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi()

        self._step = 0

    def setupUi(self):
        sz = 15  # Магическое число

        self.setGeometry(300, 300, sz * 13, sz * 17)
        self.setWindowTitle('Игра')
        self.field = [[], [], []]

        for i in range(3):
            for j in range(3):
                button = QPushButton('', self)
                self.field[i].append(button)
                self.field[i][j].resize(sz * 3, sz * 3)
                self.field[i][j].move(sz + 4 * i * sz, 3 * sz + j * 4 * sz)
                self.field[i][j].clicked.connect(
                    lambda checked, button=button, i=i, j=j: self._on_clicked_cell(button, i, j)
                )

    def _on_clicked_cell(self, button, i, j):
        print(button.text(), i, j)
        if button.text():
            return

        if self._step % 2 == 0:
            button.setText('X')
        else:
            button.setText('O')

        self._step += 1


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()