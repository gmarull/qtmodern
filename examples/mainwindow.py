import sys
from os.path import join, dirname, abspath

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication

import qtmodern.styles
import qtmodern.windows


_UI = join(dirname(abspath(__file__)), 'mainwindow.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType(_UI)


class MainWindow(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # enable High DPI support
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow())
    mw.show()

    sys.exit(app.exec_())
