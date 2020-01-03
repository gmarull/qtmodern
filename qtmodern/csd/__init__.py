from qtmodern._utils import PLATFORM

if PLATFORM == 'win32':
    from qtmodern.csd.win32 import QCSDWindow
elif PLATFORM == 'darwin':
    from qtmodern.csd.darwin import QCSDWindow
else:
    from qtmodern.csd.dummy import QCSDWindow
