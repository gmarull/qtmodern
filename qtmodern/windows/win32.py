from os.path import join, dirname, abspath

from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QToolButton
from qtpy.QtCore import Qt, Slot, QEvent, QMetaObject
from qtpy.QtGui import QIcon, QPixmap

from qtmodern._csd.win32 import QCSDWindow

_RESOURCE = join(dirname(dirname(abspath(__file__))), "resources")

_style = """
QToolButton {{
  background-color: transparent;
  border: transparent;
  padding: 0 10px;
}}

QToolButton:hover {{
  background-color: {};
  border: transparent;
}}

#btnClose:hover {{
  background-color: #d11919;
  border: transparent;
}}

"""


class _TitleBar(QWidget):
    def __init__(self, parent=None):
        super(_TitleBar, self).__init__(parent)
        self.hLayoutContent = QHBoxLayout()
        self.hLayoutContent.setSpacing(0)
        self.hLayoutContent.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hLayoutContent)

        self.applicationIcon = QToolButton()
        self.applicationIcon.setObjectName('applicationLogo')

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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

        midlight = '#%02x%02x%02x' % self.palette().midlight().color().getRgb()[:-1]
        button_style = _style.format(midlight)

        self.btnMinimize.setIcon(QIcon(QPixmap(join(_RESOURCE, "minimize.svg"))))
        self.btnRestore.setIcon(QIcon(QPixmap(join(_RESOURCE, "restore.svg"))))
        self.btnMaximize.setIcon(QIcon(QPixmap(join(_RESOURCE, "maximize.svg"))))
        self.btnClose.setIcon(QIcon(QPixmap(join(_RESOURCE, "close.svg"))))
        self.btnMinimize.setStyleSheet(button_style)
        self.btnRestore.setStyleSheet(button_style)
        self.btnMaximize.setStyleSheet(button_style)
        self.btnClose.setStyleSheet(button_style)
        self.applicationIcon.setStyleSheet("QToolButton { background-color: transparent; border: transparent;}")

        self.hLayoutContent.addWidget(self.applicationIcon)

        self.hLayoutContent.addWidget(self.lblTitle)
        self.hLayoutContent.addWidget(self.btnMinimize)
        self.hLayoutContent.addWidget(self.btnRestore)
        self.hLayoutContent.addWidget(self.btnMaximize)
        self.hLayoutContent.addWidget(self.btnClose)


class _WindowsTitleBar(_TitleBar):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self._window = window
        self._window.installEventFilter(self)

        self.applicationIcon.setIcon(self._window.windowIcon())
        self._window.windowIconChanged.connect(self.on_windowIconChanged)

        self.lblTitle.setText(self._window.windowTitle())
        self._window.windowTitleChanged.connect(self.on_windowTitleChanged)

        QMetaObject.connectSlotsByName(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowStateChange:
            if self._window.windowState() == Qt.WindowMaximized:
                self.btnMaximize.setVisible(False)
                self.btnRestore.setVisible(True)
            else:
                self.btnMaximize.setVisible(True)
                self.btnRestore.setVisible(False)

        return super().eventFilter(obj, event)

    @Slot()
    def on_btnMinimize_clicked(self):
        self._window.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        self._window.setWindowState(Qt.WindowNoState)
        self.btnMaximize.setVisible(True)
        self.btnRestore.setVisible(False)

    @Slot()
    def on_btnMaximize_clicked(self):
        self._window.setWindowState(Qt.WindowMaximized)
        self.btnMaximize.setVisible(False)
        self.btnRestore.setVisible(True)

    @Slot()
    def on_btnClose_clicked(self):
        self._window.close()

    @Slot(str)
    def on_windowTitleChanged(self, title):
        self.lblTitle.setText(title)

    @Slot(QIcon)
    def on_windowIconChanged(self, icon):
        self.applicationIcon.setIcon(icon)


class ModernWindow(QCSDWindow):
    """Main Window."""

    def __init__(self, window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = _WindowsTitleBar(self, self)

        self.addDragger(self.titlebar.lblTitle)
        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(window)