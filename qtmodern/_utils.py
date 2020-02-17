import sys
import qtpy
import platform
from os.path import join, dirname, abspath

QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """

PLATFORM = platform.system().lower()

if hasattr(sys, '_MEIPASS'):  # PyInstaller
    RESOURCES = join(sys._MEIPASS, dirname(abspath(__file__)), "resources")
elif hasattr(sys, 'frozen'):  # cx_Freeze
    RESOURCES = join(dirname(abspath(sys.executable)), "resources")
else:
    RESOURCES = join(dirname(abspath(__file__)), "resources")

FRAMELESS_STYLESHEET = join(RESOURCES, 'frameless.qss')
MODERN_STYLESHEET = join(RESOURCES, 'style.qss')
RESTORE_ICON = join(RESOURCES, 'restore.svg')
MAXIMIZE_ICON = join(RESOURCES, 'maximize.svg')


PLATFORM_WINDOWS = "windows"
PLATFORM_MACOS = "darwin"
