from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtCore import Qt, Slot, QEvent, QMetaObject
from qtpy.QtGui import QIcon
from qtmodern._utils import PLATFORM, FL_STYLESHEET, RESTORE_ICON, MAXIMIZE_ICON
from qtmodern.csd import QCSDWindow

if PLATFORM == "win32":
    from qtmodern.widgets import WindowsTitleBar as TitleBarWidget
elif PLATFORM == 'darwin':
    from qtmodern.widgets import MacOSTitleBar as TitleBarWidget
else:
    from qtmodern.widgets import WindowsTitleBar as TitleBarWidget


class ModernWindow(QCSDWindow):
    """Main Window."""

    def __init__(self, window):
        super().__init__()
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(0)
        self.setLayout(self.vLayout)
        self.titlebar = TitleBarWidget(self)

        if PLATFORM == 'win32':  # custom title bar on Windows
            self.addDragger(self.titlebar.lblTitle)

        self.vLayout.addWidget(self.titlebar)
        self.vLayout.addWidget(window)

        self._window = window
        self._window.installEventFilter(self)

        self.titlebar.lblTitle.setText(self._window.windowTitle())
        self._window.windowTitleChanged.connect(self.on_windowTitleChanged)

        # self.btnLogo.setIcon(self._window.windowIcon())
        # self._window.windowIconChanged.connect(self.on_windowIconChanged)
        # set stylesheet

        with open(FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # Automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowStateChange:
            if self._window.windowState() == Qt.WindowMaximized:
                self.titlebar.btnMaximize.setVisible(False)
                self.titlebar.btnRestore.setVisible(True)
            else:
                self.titlebar.btnMaximize.setVisible(True)
                self.titlebar.btnRestore.setVisible(False)

        return super().eventFilter(obj, event)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnRestore_clicked(self):
        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnClose_clicked(self):
        self._window.close()

    @Slot(str)
    def on_windowTitleChanged(self, title):
        self.titlebar.lblTitle.setText(title)

    # @Slot(QIcon)
    # def on_windowIconChanged(self, icon):
    #     self.btnIcon.setIcon(icon)
