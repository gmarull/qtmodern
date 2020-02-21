import qtpy
import platform
QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """


FRAMELESS_STYLESHEET = ':/stylesheets/frameless.qss'
MODERN_STYLESHEET = ':/stylesheets/style.qss'


PLATFORM = platform.system().lower()
PLATFORM_WINDOWS = "windows"
PLATFORM_MACOS = "darwin"
