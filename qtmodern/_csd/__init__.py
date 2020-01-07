from qtmodern._utils import PLATFORM, PLATFORM_MACOS, PLATFORM_WINDOWS

if PLATFORM in PLATFORM_WINDOWS:
    from qtmodern._csd.win32 import QCSDWindow
elif PLATFORM in PLATFORM_MACOS:
    from qtmodern._csd.darwin import QCSDWindow
else:
    from qtmodern._csd.dummy import QCSDWindow
