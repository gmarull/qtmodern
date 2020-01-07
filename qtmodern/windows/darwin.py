from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QSizePolicy
from qtpy.QtCore import Qt, Slot

from qtmodern._csd.darwin import QCSDWindow


class _MacOSTitleBar(QWidget):
    _HEIGHT = 22
    """int: Height."""

    def __init__(self, window, parent=None):
        super().__init__(parent)

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)

        self.frmContent = QFrame(self)
        self.frmContent.setObjectName('frmContent')
        self.hLayoutContent = QHBoxLayout()
        self.hLayoutContent.setContentsMargins(0, 0, 0, 0)

        self.lblTitle = QLabel(self.frmContent)
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lblTitle.setFixedHeight(self._HEIGHT)
        self.lblTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lblTitle.setText(window.windowTitle())
        window.windowTitleChanged.connect(self.on_windowTitleChanged)
        self.hLayout.addWidget(self.frmContent)
        self.frmContent.setLayout(self.hLayoutContent)
        self.hLayoutContent.addWidget(self.lblTitle)

    @Slot(str)
    def on_windowTitleChanged(self, title):
        self.lblTitle.setText(title)


class ModernWindow(QCSDWindow):
    def __init__(self, window):
        super().__init__()
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.titlebar = _MacOSTitleBar(self, self)

        self.hLayout.addWidget(self.titlebar)
        self.hLayout.addWidget(window)