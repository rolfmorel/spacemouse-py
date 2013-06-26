import sys

from types import ModuleType

from .wrapper import spacemouse_monitor_open

monitor_fd = -1

monitor_add_callback = None
monitor_remove_callback = None


class Monitor(ModuleType):
    def __init__(self, module):
        self.__module__ = module
        self.__name__ = module.__name__

    def __call__(self, add=None, remove=None, thread=None):
        global monitor_fd, monitor_add_callback, monitor_remove_callback

        if add is None and remove is None:
            raise ValueError("atleast one of add or remove arguments needed")
        if add is not None:
            if not callable(add):
                raise TypeError("add argument must be callable")
            monitor_add_callback = add
        if remove is not None:
            if not callable(remove):
                raise TypeError("remove argument must be callable")
            monitor_remove_callback = remove

        if monitor_fd == -1:
            monitor_fd = spacemouse_monitor_open()

        if thread is not None:
            from .background import background_thread, BackgroundThread
            if background_thread is None:
                thread = BackgroundThread()
            else:
                thread = background_thread
        return thread

    def __getattr__(self, attr):
        return getattr(self.__module__, attr)


sys.modules[__name__] = Monitor(sys.modules[__name__])
