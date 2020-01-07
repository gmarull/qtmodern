from qtmodern._utils import PLATFORM, PLATFORM_MACOS, PLATFORM_WINDOWS

if PLATFORM in PLATFORM_WINDOWS:
    from qtmodern.windows.win32 import ModernWindow
elif PLATFORM in PLATFORM_MACOS:
    from qtmodern.windows.darwin import ModernWindow
else:
    from qtmodern.windows.dummy import ModernWindow
