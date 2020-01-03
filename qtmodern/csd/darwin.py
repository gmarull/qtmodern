import objc
import Cocoa
import ctypes

from qtpy.QtCore import QEvent
from qtpy.QtWidgets import QWidget

# from PyQt5.QtCore import Qt
# print(Qt.WA_TranslucentBackground)

class QCSDWindow(QWidget):
    """CSD Window (macOS)."""

    def __init__(self, parent=None):
        super().__init__(parent)

        view = objc.objc_object(c_void_p=ctypes.c_void_p(int(self.winId())))
        self._window = view.window()
        self._hideTitlebar()

    def changeEvent(self, event):
        super().changeEvent(event)
        # FIX for QTBUG-69975
        if event.type() == QEvent.WindowStateChange:
            self._hideTitlebar()

    def paintEvent(self, event):
        super().paintEvent(event)
        # FIX: titlebar re-appears on some occasions
        self._window.setTitlebarAppearsTransparent_(True)

    def _hideTitlebar(self):
        """Hide titlebar."""
        self._window.setStyleMask_(
            self._window.styleMask() |
            Cocoa.NSFullSizeContentViewWindowMask)
        self._window.setTitlebarAppearsTransparent_(True)
        self._window.setTitleVisibility_(Cocoa.NSWindowTitleHidden)