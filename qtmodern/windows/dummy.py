from qtpy.QtWidgets import QVBoxLayout

from qtmodern._csd.dummy import QCSDWindow


class ModernWindow(QCSDWindow):
    def __init__(self, window):
        super().__init__()
        self.h_layout = QVBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(0)
        self.h_layout.addWidget(window)
