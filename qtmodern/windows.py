from os.path import join, dirname, abspath

from qtpy.QtCore import Qt, QMetaObject, Signal, Slot
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                            QLabel, QSizePolicy)

from ._utils import QT_VERSION


_FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/frameless.qss')
""" str: Frameless window stylesheet. """


class WindowDragger(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    doubleClicked = Signal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(self._windowPos +
                              (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, w, parent=None):
        QWidget.__init__(self, parent)

        self.setupUi()
        self.setupEvents(w)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Fixed))
                   
        # START ADD
        self.titleBar.setStyleSheet("background-color: white; margin-top:1px")
        # END ADD

        # START ADD
        self.titleBar.setStyleSheet("background-color: white; margin-top:1px")
        # END ADD

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignCenter)
        
        # START ADD
        self.lblTitle.setAlignment(Qt.AlignVCenter)
        self.lblTitle.setPixmap(QPixmap(":/newPrefix/jubot_large_rounded_square_converted.png"))
        
        self.icon = QLabel()
        self.icon.setMinimumSize(QSize(32, 37))
        self.icon.setMaximumSize(QSize(32, 37))
        self.icon.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.icon.setStyleSheet("padding-left: 10px; padding-right: 1px; padding-top:8px; padding-bottom: 8px; background-color: white; margin-top:1px; margin-left:1px")
        self.icon.setPixmap(QPixmap(":/newPrefix/jubot_large_rounded_square_converted.png"))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")
        
        self.hboxTitle.addWidget(self.icon)
        # END ADD
        
        self.hboxTitle.addWidget(self.lblTitle)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        
        # START ADD
        self.btnMinimize.setIcon(QPixmap(":/newPrefix/windows10_min_button.png"))
        self.btnMinimize.setIconSize(QSize(55,33))
        self.btnMinimize.setCursor(QCursor(Qt.PointingHandCursor))
        # END ADD
        
        self.btnMinimize.setSizePolicy(spButtons)
        self.hboxTitle.addWidget(self.btnMinimize)

        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        self.hboxTitle.addWidget(self.btnRestore)

        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)
        
        # START ADD
        self.btnMaximize.hide()
        # END ADD
        
        self.hboxTitle.addWidget(self.btnMaximize)

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        
        # START ADD
        self.btnClose.setIcon(QPixmap(":/newPrefix/windows10_close_button.png"))
        self.btnClose.setIconSize(QSize(55,33))
        self.btnClose.setCursor(QCursor(Qt.PointingHandCursor))
        # END ADD
        
        self.btnClose.setSizePolicy(spButtons)
        self.hboxTitle.addWidget(self.btnClose)

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)

        # set window flags
        self.setWindowFlags(
                Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        if QT_VERSION >= (5,):
            self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def setupEvents(self, w):
        w.close = self.close
        self.closeEvent = w.closeEvent

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        self.lblTitle.setText(title)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        self.btnMaximize.setVisible(False)

        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if self.btnMaximize.isVisible():
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()
