# Errors

## macOS

Can not run with `PySide2>=5.12.6` or `pyqt5==5.13.2` because of an error/crash.
```
2020-01-09 15:44:48.773 Python[30625:1737933] It does not make sense to draw an image when [NSGraphicsContext currentContext] is nil.  This is a programming error. Break on void _NSWarnForDrawingImageWithNoCurrentContext(void) to debug.  This will be logged only once.  This may break in the future.
QThread: Destroyed while thread is still running
```

`PySide2` reports the following error
```
Qt WebEngine seems to be initialized from a plugin. Please set Qt::AA_ShareOpenGLContexts using QCoreApplication::setAttribute before constructing QGuiApplication.
``` 