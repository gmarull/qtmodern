import sys
import qtpy
import platform
from os.path import join, dirname, abspath
QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """


FRAMELESS_STYLESHEET = ':/stylesheets/frameless.qss'
MODERN_STYLESHEET = ':/stylesheets/style.qss'
RESTORE_ICON = ':/icons/restore.svg'
MAXIMIZE_ICON = ':/icons/maximize.svg'
CLOSE_ICON = ':/icons/maximize.svg'
MINIMIZE_ICON = ':/icons/minimize.svg'


PLATFORM = platform.system().lower()
PLATFORM_WINDOWS = "windows"
PLATFORM_MACOS = "darwin"
