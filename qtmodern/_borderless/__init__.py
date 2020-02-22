from qtmodern._utils import PLATFORM, PLATFORM_MACOS, PLATFORM_WINDOWS

if PLATFORM in PLATFORM_WINDOWS:
    from qtmodern._borderless.win32 import BorderlessWindow
elif PLATFORM in PLATFORM_MACOS:
    from qtmodern._borderless.darwin import BorderlessWindow
else:
    from qtmodern._borderless.dummy import BorderlessWindow
