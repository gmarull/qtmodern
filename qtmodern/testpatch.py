"""
Test patch for qtmodern

If a widget to be wrapped by a ModernWindow object has a non-empty title.
Then the ModernWindow widget will preserve this title after wrapping.

Maxwell Grady
September 22, 2017
"""

import sys
from PyQt5 import QtWidgets
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

def main():
    app = QtWidgets.QApplication([])
    dark(app)

    # create widget to be wrapped by ModernWindow
    # set widget title before wrapping
    widget = QtWidgets.QWidget()
    widget.setWindowTitle("QWidgetTitle")

    modwin = ModernWindow(widget)
    modwin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
