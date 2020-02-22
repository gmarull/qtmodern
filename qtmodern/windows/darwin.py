from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QSizePolicy
from qtpy.QtCore import Qt

from qtmodern._borderless.darwin import BorderlessWindow


class _MacOSTitleBar(QWidget):
    _HEIGHT = 22

    def __init__(self, modern_window, user_window):
        super().__init__(modern_window)

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_content = QFrame(self)
        self.frame_content.setObjectName('frmContent')
        self.h_layout_content = QHBoxLayout()
        self.h_layout_content.setContentsMargins(0, 0, 0, 0)

        self.lbl_title = QLabel(self.frame_content)
        self.lbl_title.setObjectName('lblTitle')
        self.lbl_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lbl_title.setFixedHeight(self._HEIGHT)
        self.lbl_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lbl_title.setText(user_window.windowTitle())
        self.h_layout.addWidget(self.frame_content)
        self.frame_content.setLayout(self.h_layout_content)
        self.h_layout_content.addWidget(self.lbl_title)

        user_window.windowTitleChanged.connect(self.on_window_title_changed)

    def on_window_title_changed(self, title):
        self.lbl_title.setText(title)


class ModernWindow(BorderlessWindow):
    def __init__(self, user_window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = _MacOSTitleBar(self, user_window)

        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(user_window)
