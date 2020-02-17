import sys
import qtpy
import platform
from os.path import join, dirname, abspath

QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """

PLATFORM = platform.system().lower()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, dirname(abspath(__file__)), relative_path)
    return join(dirname(abspath(__file__)), relative_path)

RESOURCES = join(dirname(abspath(__file__)), 'resources')
FL_STYLESHEET = join(RESOURCES, 'frameless.qss')
RESTORE_ICON = join(RESOURCES, 'restore.svg')
MAXIMIZE_ICON = join(RESOURCES, 'maximize.svg')


PLATFORM_WINDOWS = "windows"
PLATFORM_MACOS = "darwin"
