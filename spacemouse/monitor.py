import sys
from types import ModuleType

from . import backend, register
from .list import device_list
from .device import Device

if backend.get('monitor') == "udev":
    from .udev.monitor import Monitor as BackendMonitor
else:
    raise ValueError("No valid 'monitor' backend specified")


class Monitor(BackendMonitor, ModuleType):
    add_cb = None
    remove_cb = None

    def __init__(self, module):
        super(Monitor, self).__init__()

        self.__module__ = module
        self.__name__ = module.__name__

    def __call__(self, add=None, remove=None):
        if add is None and remove is None:
            raise ValueError("atleast one of 'add' or 'remove' arguments "
                             "needed")

        if add is not None:
            if not callable(add):
                raise TypeError("'add' argument must be callable")

            self.add_cb = add

        if remove is not None:
            if not callable(remove):
                raise TypeError("'remove' argument must be callable")

            self.remove_cb = remove

    def read_one(self, valid_only=True):
        action, match = super(Monitor, self).read_one(valid_only=valid_only)

        if action is None:
            return None, None

        dev = Device(*match)

        for idx, device in enumerate(device_list):
            if dev == device:
                if action == "remove":
                    del device_list[idx]
                elif action == "add":
                    raise RuntimeError("can not add a device which is already "
                                       "in the list")

                return action, device
        else:
            if action == "add":
                device_list.append(dev)

                register.update(dev)

        return action, dev

    def read(self, valid_only=True):
        read_gen = iter(super(Monitor, self).read(valid_only=valid_only),
                        (None, (None, None, None)))

        for action, match in read_gen:
            dev = Device(*match)

            for idx, device in enumerate(device_list):
                if dev == device:
                    if action == "remove":
                        del device_list[idx]

                    yield action, device
            else:
                if action == "add":
                    device_list.append(dev)

                    register.update(dev)
                yield action, dev

    def dispatch(self, action=None, device=None):
        if action is None:
            action, device = self.read_one(valid_only=False)

        if action == 'add' and self.add_cb is not None:
            self.add_cb(device)
        elif action == 'remove' and self.remove_cb is not None:
            self.remove_cb(device)

    def __getattr__(self, attr):
        return getattr(self.__module__, attr)


sys.modules[__name__] = Monitor(sys.modules[__name__])
