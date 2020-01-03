import sys
from time import sleep
from os.path import join, dirname, abspath, basename, isdir
from os import listdir

from qtpy import uic
from qtpy.QtCore import Slot, QThread, Signal
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem

import qtmodern.styles
from qtmodern.csdwindows import ModernWindow


_UI = join(dirname(abspath(__file__)), 'mainwindow.ui')


class ProgressThread(QThread):
    update = Signal(int)

    def run(self):
        progress = 20
        while True:
            progress += 1
            if progress == 100:
                progress = 0

            self.update.emit(progress)
            sleep(0.5)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        uic.loadUi(_UI, self)  # Load the ui into self

        self.tooltiplabel.setToolTip("This is a tool tip that shows a tip about the tool")

        self.actionLight.triggered.connect(self.lightTheme)
        self.actionDark.triggered.connect(self.darkTheme)

        self.thread = ProgressThread()
        self.thread.update.connect(self.update_progress)
        self.thread.start()

        self.load_project_structure(dirname(dirname(abspath(__file__))), self.treeWidget)

        for i in range(100):
            self.comboBox_2.addItem("item {}".format(i))

    def load_project_structure(self, startpath, tree):
        for element in listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QTreeWidgetItem(tree, [basename(element)])
            if isdir(path_info):
                self.load_project_structure(path_info, parent_itm)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def lightTheme(self):
        qtmodern.styles.light(QApplication.instance())

    def darkTheme(self):
        qtmodern.styles.dark(QApplication.instance())

    @Slot()
    def on_pushButton_clicked(self):
        self.close()

    @Slot()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Do you want to exit?')

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    qtmodern.styles.dark(app)
    mw = ModernWindow(MainWindow())
    mw.show()

    sys.exit(app.exec_())
