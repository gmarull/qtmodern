from qtpy.QtCore import Qt, QMetaObject, Signal, Slot
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QSizePolicy, QDialog, QMessageBox)
from ._utils import QT_VERSION, PLATFORM, resource_path


_FL_STYLESHEET = resource_path('resources/frameless.qss')
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


class TitleBar(WindowDragger):
    """ Window titlebar.
        Args:
            window (QWidget): The window to attach to.
    """
    def __init__(self, window):
        super().__init__(window, window.windowFrame)
        self.window = window
        self.setupUi()

    def setupUi(self):
        self.setObjectName('titleBar')
        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

        self.window.hboxTitle = QHBoxLayout(self)
        self.window.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.window.hboxTitle.setSpacing(0)

        self.window.lblTitle = QLabel('Title')
        self.window.lblTitle.setObjectName('lblTitle')
        self.window.lblTitle.setAlignment(Qt.AlignCenter)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.window.btnMinimize = QToolButton(self)
        self.window.btnMinimize.setObjectName('btnMinimize')
        self.window.btnMinimize.setSizePolicy(spButtons)

        self.window.btnRestore = QToolButton(self)
        self.window.btnRestore.setObjectName('btnRestore')
        self.window.btnRestore.setSizePolicy(spButtons)

        self.window.btnMaximize = QToolButton(self)
        self.window.btnMaximize.setObjectName('btnMaximize')
        self.window.btnMaximize.setSizePolicy(spButtons)

        self.window.btnClose = QToolButton(self)
        self.window.btnClose.setObjectName('btnClose')
        self.window.btnClose.setSizePolicy(spButtons)

        self.window.vboxFrame.addWidget(self)

        self.window.windowContent = QWidget(self.window.windowFrame)
        self.window.vboxFrame.addWidget(self.window.windowContent)

        self.window.vboxWindow.addWidget(self.window.windowFrame)

        if PLATFORM == "Darwin":
            self.window.hboxTitle.addWidget(self.window.btnClose)
            self.window.hboxTitle.addWidget(self.window.btnMinimize)
            self.window.hboxTitle.addWidget(self.window.btnRestore)
            self.window.hboxTitle.addWidget(self.window.btnMaximize)
            self.window.hboxTitle.addWidget(self.window.lblTitle)
        else:
            self.window.hboxTitle.addWidget(self.window.lblTitle)
            self.window.hboxTitle.addWidget(self.window.btnMinimize)
            self.window.hboxTitle.addWidget(self.window.btnRestore)
            self.window.hboxTitle.addWidget(self.window.btnMaximize)
            self.window.hboxTitle.addWidget(self.window.btnClose)


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, w, parent=None):
        QWidget.__init__(self, parent)

        self._w = w
        self.setupUi()

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())

        # Adding attribute to clean up the parent window when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self.__child_was_closed)

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = TitleBar(self)

        # set window flags
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        if QT_VERSION >= (5,):
            self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None  # The child was deleted, remove the reference to it and close the parent window
        self.close()

    def closeEvent(self, event):
        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        super(ModernWindow, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    def _setWindowButtonState(self, hint, state):
        btns = {
            Qt.WindowCloseButtonHint: self.btnClose,
            Qt.WindowMinimizeButtonHint: self.btnMinimize,
            Qt.WindowMaximizeButtonHint: self.btnMaximize
        }
        button = btns.get(hint)

        maximized = bool(self.windowState() & Qt.WindowMaximized)

        if button == self.btnMaximize:  # special rules for max/restore
            self.btnRestore.setEnabled(state)
            self.btnMaximize.setEnabled(state)

            if maximized:
                self.btnRestore.setVisible(state)
                self.btnMaximize.setVisible(False)
            else:
                self.btnMaximize.setVisible(state)
                self.btnRestore.setVisible(False)
        else:
            button.setEnabled(state)

        allButtons = [self.btnClose, self.btnMinimize, self.btnMaximize, self.btnRestore]
        if True in [b.isEnabled() for b in allButtons]:
            for b in allButtons:
                b.setVisible(True)
            if maximized:
                self.btnMaximize.setVisible(False)
            else:
                self.btnRestore.setVisible(False)
            self.lblTitle.setContentsMargins(0, 0, 0, 0)
        else:
            for b in allButtons:
                b.setVisible(False)
            self.lblTitle.setContentsMargins(0, 2, 0, 0)

    def setWindowFlag(self, Qt_WindowType, on=True):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]

        if Qt_WindowType in buttonHints:
            self._setWindowButtonState(Qt_WindowType, on)
        else:
            QWidget.setWindowFlag(self, Qt_WindowType, on)

    def setWindowFlags(self, Qt_WindowFlags):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]
        for hint in buttonHints:
            self._setWindowButtonState(hint, bool(Qt_WindowFlags & hint))

        QWidget.setWindowFlags(self, Qt_WindowFlags)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        if self.btnMaximize.isEnabled() or self.btnRestore.isEnabled():
            self.btnRestore.setVisible(False)
            self.btnRestore.setEnabled(False)
            self.btnMaximize.setVisible(True)
            self.btnMaximize.setEnabled(True)

        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        if self.btnMaximize.isEnabled() or self.btnRestore.isEnabled():
            self.btnRestore.setVisible(True)
            self.btnRestore.setEnabled(True)
            self.btnMaximize.setVisible(False)
            self.btnMaximize.setEnabled(False)

        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if not bool(self.windowState() & Qt.WindowMaximized):
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()


class ModernDialog(QDialog):
    """ Modern window.

        Args:
            w (QDialog): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi()

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = TitleBar(self)

        # set window flags
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        if QT_VERSION >= (5,):
            self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None  # The child was deleted, remove the reference to it and close the parent window
        self.close()

    def closeEvent(self, event):
        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        super(ModernDialog, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    def _setWindowButtonState(self, hint, state):
        btns = {
            Qt.WindowCloseButtonHint: self.btnClose,
            Qt.WindowMinimizeButtonHint: self.btnMinimize,
            Qt.WindowMaximizeButtonHint: self.btnMaximize
        }
        button = btns.get(hint)

        maximized = bool(self.windowState() & Qt.WindowMaximized)

        if button == self.btnMaximize:  # special rules for max/restore
            self.btnRestore.setEnabled(state)
            self.btnMaximize.setEnabled(state)

            if maximized:
                self.btnRestore.setVisible(state)
                self.btnMaximize.setVisible(False)
            else:
                self.btnMaximize.setVisible(state)
                self.btnRestore.setVisible(False)
        else:
            button.setEnabled(state)

        allButtons = [self.btnClose, self.btnMinimize, self.btnMaximize, self.btnRestore]
        if True in [b.isEnabled() for b in allButtons]:
            for b in allButtons:
                b.setVisible(True)
            if maximized:
                self.btnMaximize.setVisible(False)
            else:
                self.btnRestore.setVisible(False)
            self.lblTitle.setContentsMargins(0, 0, 0, 0)
        else:
            for b in allButtons:
                b.setVisible(False)
            self.lblTitle.setContentsMargins(0, 2, 0, 0)

    def setWindowFlag(self, Qt_WindowType, on=True):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]

        if Qt_WindowType in buttonHints:
            self._setWindowButtonState(Qt_WindowType, on)
        else:
            QWidget.setWindowFlag(self, Qt_WindowType, on)

    def setWindowFlags(self, Qt_WindowFlags):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]
        for hint in buttonHints:
            self._setWindowButtonState(hint, bool(Qt_WindowFlags & hint))

        QWidget.setWindowFlags(self, Qt_WindowFlags)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        if self.btnMaximize.isEnabled() or self.btnRestore.isEnabled():
            self.btnRestore.setVisible(False)
            self.btnRestore.setEnabled(False)
            self.btnMaximize.setVisible(True)
            self.btnMaximize.setEnabled(True)

        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        if self.btnMaximize.isEnabled() or self.btnRestore.isEnabled():
            self.btnRestore.setVisible(True)
            self.btnRestore.setEnabled(True)
            self.btnMaximize.setVisible(False)
            self.btnMaximize.setEnabled(False)

        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if not bool(self.windowState() & Qt.WindowMaximized):
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()


class ModernMessageBox(QMessageBox):
    """ Modern message box.
        Args:
            parent (QWidget, optional): Parent widget.
    """
    def __init__(self, parent=None):
        self._dialog = ModernDialog(parent=parent)
        QMessageBox.__init__(self, self._dialog)

        self.setupUi()

    def setupUi(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self, alignment=Qt.AlignCenter)
        self._dialog.windowContent.setLayout(layout)

        self._dialog.show()

    def hide(self):
        QMessageBox.hide(self)
        self._dialog.hide()
