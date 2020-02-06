import sys
from os.path import join, dirname, abspath
import qtpy
import platform

QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """

PLATFORM = platform.system()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, dirname(abspath(__file__)), relative_path)
    return join(dirname(abspath(__file__)), relative_path)
