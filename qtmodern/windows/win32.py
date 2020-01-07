from qtpy.QtWidgets import QVBoxLayout

from qtmodern.csd.win32 import QCSDWindow
from qtmodern.widgets import WindowsTitleBar as TitleBarWidget


class ModernWindow(QCSDWindow):
    """Main Window."""

    def __init__(self, window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = TitleBarWidget(self, self)

        self.addDragger(self.titlebar.lblTitle)
        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(window)