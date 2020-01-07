import ctypes as ct
from ctypes import windll
from ctypes.wintypes import MSG, RECT

from qtpy.QtCore import qVersion, QEvent, Qt
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget

# Windows Window Manager constants
WM_NCCALCSIZE = 131
WM_NCHITTEST = 132

HTCAPTION = 2
HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17


class MARGINS(ct.Structure):
    _fields_ = [('cxLeftWidth', ct.c_int),
                ('cxRightWidth', ct.c_int),
                ('cyTopHeight', ct.c_int),
                ('cyBottomHeight', ct.c_int)]


class QCSDWindow(QWidget):
    _DEF_BORDER_WIDTH = 8
    """int: Default border width (for resize)."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._borderWidth = self._DEF_BORDER_WIDTH
        self._draggers = []

        # enable CSD
        hWnd = ct.c_int(self.winId())
        margins = MARGINS(-1, -1, -1, -1)
        windll.dwmapi.DwmExtendFrameIntoClientArea(hWnd, ct.byref(margins))

    def changeEvent(self, event):
        # FIX: adjust window margins on Windows
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowMaximized:
                self.setContentsMargins(7, 7, 7, 7)
            else:
                self.setContentsMargins(0, 0, 0, 0)

        return super().changeEvent(event)

    def nativeEvent(self, eventType, message):
        # FIX: QTBUG-69074
        if qVersion() in ('5.11.0', '5.11.1'):
            msg = ct.POINTER(MSG).from_address(int(message))[0]
        else:
            msg = MSG.from_address(int(message))

        if msg.message == WM_NCCALCSIZE:
            return True, 0

        if msg.message == WM_NCHITTEST:
            wr = RECT()
            windll.user32.GetWindowRect(msg.hWnd, ct.byref(wr))

            ht = None
            x = (msg.lParam & 0xFFFF)
            y = (msg.lParam >> 16)

            if (wr.left <= x < wr.left + self._borderWidth and
                    wr.bottom > y >= wr.bottom - self._borderWidth):
                ht = HTBOTTOMLEFT
            elif (wr.right > x >= wr.right - self._borderWidth and
                  wr.bottom > y >= wr.bottom - self._borderWidth):
                ht = HTBOTTOMRIGHT
            elif (wr.left <= x < wr.left + self._borderWidth and
                  wr.top <= y < wr.top + self._borderWidth):
                ht = HTTOPLEFT
            elif (wr.right > x >= wr.right - self._borderWidth and
                  wr.top <= y < wr.top + self._borderWidth):
                ht = HTTOPRIGHT
            elif wr.left <= x < wr.left + self._borderWidth:
                ht = HTLEFT
            elif wr.right > x >= wr.right - self._borderWidth:
                ht = HTRIGHT
            elif wr.bottom > y >= wr.bottom - self._borderWidth:
                ht = HTBOTTOM
            elif wr.top <= y < wr.top + self._borderWidth:
                ht = HTTOP
            elif QApplication.instance().widgetAt(QCursor.pos()) in self._draggers:
                ht = HTCAPTION

            if ht is not None:
                return True, ht

        return False, 0

    def addDragger(self, widget):
        self._draggers.append(widget)
