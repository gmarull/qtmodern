import qtpy
import platform

QT_VERSION = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))
""" tuple: Qt version. """

PLATFORM = platform.system()
