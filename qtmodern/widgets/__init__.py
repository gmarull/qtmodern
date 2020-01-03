"""Titlebar Widget."""
from os.path import join, dirname, abspath
from qtpy.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QSizePolicy, QToolButton, QVBoxLayout
from qtpy.QtCore import Qt, Slot, QEvent
from qtpy.QtGui import QIcon
from qtpy import uic

_RESOURCE = join(dirname(dirname(abspath(__file__))), "resources")
_TITLEBAR_WIDGET = join(_RESOURCE, 'TitlebarWidget.ui')
_FL_STYLESHEET = join(_RESOURCE, 'frameless.qss')


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)
        # self.frmContent = QFrame(self)
        # self.frmContent.setObjectName('frmContent')
        self.hLayoutContent = QHBoxLayout()
        self.hLayoutContent.setSpacing(0)
        self.hLayoutContent.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hLayoutContent)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lblTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton()
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)

        self.btnRestore = QToolButton()
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)

        self.btnMaximize = QToolButton()
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)

        self.btnClose = QToolButton()
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)


class WindowsTitleBar(TitleBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("windows")
        self.hLayoutContent.addWidget(self.lblTitle)
        self.hLayoutContent.addWidget(self.btnMinimize)
        self.hLayoutContent.addWidget(self.btnRestore)
        self.hLayoutContent.addWidget(self.btnMaximize)
        self.hLayoutContent.addWidget(self.btnClose)


class MacOSTitleBar(TitleBar):
    _HEIGHT = 22
    """int: Height."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hLayoutContent.addWidget(self.btnClose)
        self.hLayoutContent.addWidget(self.btnMinimize)
        self.hLayoutContent.addWidget(self.btnRestore)
        self.hLayoutContent.addWidget(self.btnMaximize)
        self.hLayoutContent.addWidget(self.lblTitle)
        self.lblTitle.setFixedHeight(self._HEIGHT)
