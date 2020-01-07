from qtmodern._utils import PLATFORM, PLATFORM_MACOS, PLATFORM_WINDOWS

if PLATFORM in PLATFORM_WINDOWS:
    from qtmodern.csd.win32 import QCSDWindow
elif PLATFORM in PLATFORM_MACOS:
    from qtmodern.csd.darwin import QCSDWindow
else:
    from qtmodern.csd.dummy import QCSDWindow
