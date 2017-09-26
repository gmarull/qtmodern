import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtWidgets import QApplication, QMainWindow

import qtmodern.styles
import qtmodern.windows


_UI = join(dirname(abspath(__file__)), 'mainwindow.ui')


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        uic.loadUi(_UI, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow())
    mw.show()

    sys.exit(app.exec_())
