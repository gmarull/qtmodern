from qtpy.QtWidgets import QHBoxLayout
from qtmodern._utils import PLATFORM
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
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = TitleBarWidget(self, self)
        if PLATFORM == 'win32':  # custom title bar on Windows
            self.addDragger(self.titlebar.lblTitle)
        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(window)
