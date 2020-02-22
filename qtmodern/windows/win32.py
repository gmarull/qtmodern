from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,QLabel, QSizePolicy, QToolButton
from qtpy.QtCore import Qt, QEvent
from qtpy.QtGui import QIcon, QPixmap

from qtmodern._borderless.win32 import BorderlessWindow
from qtmodern._utils import MINIMIZE_ICON, CLOSE_ICON, MAXIMIZE_ICON, RESTORE_ICON
import qtmodern._resources_rc

_style = """
QToolButton {{
  background-color: transparent;
  border: transparent;
  padding: 0 10px;
  height: 25px;
}}

QToolButton:hover {{
  background-color: {};
  border: transparent;
}}

#btnClose:hover {{
  background-color: #d11919;
  border: transparent;
}}

"""


class _TitleBar(QWidget):
    def __init__(self, parent=None):
        super(_TitleBar, self).__init__(parent)
        self.h_layout_content = QHBoxLayout()
        self.title_layout_content = QHBoxLayout()
        self.title_layout_content.setSpacing(5)
        self.title_layout_content.setContentsMargins(5, 0, 0, 0)
        self.h_layout_content.setSpacing(0)
        self.h_layout_content.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.h_layout_content)

        self.application_icon = QToolButton()
        self.application_icon.setObjectName('applicationLogo')

        self.lbl_title = QLabel('Title')
        self.lbl_title.setObjectName('lblTitle')
        self.lbl_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        sp_buttons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btn_minimize = QToolButton()
        self.btn_minimize.setObjectName('btnMinimize')
        self.btn_minimize.setSizePolicy(sp_buttons)

        self.btn_restore = QToolButton()
        self.btn_restore.setObjectName('btnRestore')
        self.btn_restore.setSizePolicy(sp_buttons)
        self.btn_restore.setVisible(False)

        self.btn_maximize = QToolButton()
        self.btn_maximize.setObjectName('btnMaximize')
        self.btn_maximize.setSizePolicy(sp_buttons)

        self.btn_close = QToolButton()
        self.btn_close.setObjectName('btnClose')
        self.btn_close.setSizePolicy(sp_buttons)

        color = '#%02x%02x%02x' % self.palette().midlight().color().getRgb()[:-1]
        button_style = _style.format(color)

        self.btn_minimize.setIcon(QIcon(QPixmap(MINIMIZE_ICON)))
        self.btn_restore.setIcon(QIcon(QPixmap(RESTORE_ICON)))
        self.btn_maximize.setIcon(QIcon(QPixmap(MAXIMIZE_ICON)))
        self.btn_close.setIcon(QIcon(QPixmap(CLOSE_ICON)))
        self.btn_minimize.setStyleSheet(button_style)
        self.btn_restore.setStyleSheet(button_style)
        self.btn_maximize.setStyleSheet(button_style)
        self.btn_close.setStyleSheet(button_style)
        self.application_icon.setStyleSheet("QToolButton { background-color: transparent; border: transparent;}")

        self.title_layout_content.addWidget(self.application_icon)

        self.title_layout_content.addWidget(self.lbl_title)
        self.h_layout_content.addLayout(self.title_layout_content)
        self.h_layout_content.addWidget(self.btn_minimize)
        self.h_layout_content.addWidget(self.btn_restore)
        self.h_layout_content.addWidget(self.btn_maximize)
        self.h_layout_content.addWidget(self.btn_close)


class _WindowsTitleBar(_TitleBar):
    def __init__(self, modern_window, user_window):
        super().__init__(modern_window)
        self.user_window = user_window
        self.modern_window = modern_window
        self.modern_window.installEventFilter(self)

        self.application_icon.setIcon(self.user_window.windowIcon())
        self.user_window.windowIconChanged.connect(self.on_window_icon_changed)

        self.lbl_title.setText(self.user_window.windowTitle())
        self.user_window.windowTitleChanged.connect(self.on_window_title_changed)

        self.btn_minimize.clicked.connect(self.on_btn_minimize_clicked)
        self.btn_restore.clicked.connect(self.on_btn_restore_clicked)
        self.btn_maximize.clicked.connect(self.on_btn_maximize_clicked)
        self.btn_close.clicked.connect(self.on_btn_close_clicked)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowStateChange:
            if self.modern_window.windowState() == Qt.WindowMaximized:
                self.btn_maximize.setVisible(False)
                self.btn_restore.setVisible(True)
            else:
                self.btn_maximize.setVisible(True)
                self.btn_restore.setVisible(False)

            # Force reset hover states
            self.btn_restore.setAttribute(Qt.WA_UnderMouse, False)
            self.btn_maximize.setAttribute(Qt.WA_UnderMouse, False)

        return super().eventFilter(obj, event)

    def on_btn_minimize_clicked(self):
        self.modern_window.setWindowState(Qt.WindowMinimized)

    def on_btn_restore_clicked(self):
        self.modern_window.setWindowState(Qt.WindowNoState)
        self.btn_maximize.setVisible(True)
        self.btn_restore.setVisible(False)

    def on_btn_maximize_clicked(self):
        self.modern_window.setWindowState(Qt.WindowMaximized)
        self.btn_maximize.setVisible(False)
        self.btn_restore.setVisible(True)

    def on_btn_close_clicked(self):
        self.modern_window.close()

    def on_window_title_changed(self, title):
        self.lbl_title.setText(title)

    def on_window_icon_changed(self, icon):
        self.application_icon.setIcon(icon)


class ModernWindow(BorderlessWindow):
    def __init__(self, user_window):
        super().__init__()
        self.user_window = user_window
        self.hLayout = QVBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.title_bar = _WindowsTitleBar(self, self.user_window)

        self.add_window_mover(self.title_bar.lbl_title)
        self.hLayout.addWidget(self.title_bar)
        self.hLayout.addWidget(self.user_window)

    def closeEvent(self, event):
        self.user_window.close()
        event.setAccepted(self.user_window.isHidden())
