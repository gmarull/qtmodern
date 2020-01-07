from qtpy.QtWidgets import QVBoxLayout

from qtmodern.csd.darwin import QCSDWindow
from qtmodern.widgets import MacOSTitleBar as TitleBarWidget


class ModernWindow(QCSDWindow):
    """Main Window."""

    def __init__(self, window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = TitleBarWidget(self, self)

        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(window)