import qtpy
import platform
from os.path import join, dirname, abspath

QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """

PLATFORM = platform.system().lower()

RESOURCES = join(dirname(abspath(__file__)), 'resources')
FL_STYLESHEET = join(RESOURCES, 'frameless.qss')
RESTORE_ICON = join(RESOURCES, 'restore.svg')
MAXIMIZE_ICON = join(RESOURCES, 'maximize.svg')
