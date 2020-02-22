from qtpy.QtWidgets import QVBoxLayout

from qtmodern._borderless.dummy import BorderlessWindow


class ModernWindow(BorderlessWindow):
    def __init__(self, user_window):
        super().__init__(user_window)
        self.h_layout = QVBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(0)
        self.h_layout.addWidget(user_window)
