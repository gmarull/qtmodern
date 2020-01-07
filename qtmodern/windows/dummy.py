from qtpy.QtWidgets import QVBoxLayout

from qtmodern._csd.dummy import QCSDWindow


class ModernWindow(QCSDWindow):
    """Main Window."""

    def __init__(self, window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)
        self.hLayout.addWidget(window)