import sys
from types import ModuleType

from .list import device_list
from .registry import Registry


class Register(ModuleType):
    def __init__(self, module):
        self.__module__ = module
        self.__name__ = module.__name__

        self.registry = Registry()

    def __call__(self, callback, condition, n=None, millis=None, name=None):
        self.registry(callback, condition, n, millis, name)

        for device in device_list:
            device.register(callback, condition, n=n, millis=millis, name=name)

    def update(self, device=None):
        dev_list = [device] if device is not None else device_list

        for dev in dev_list:
            for reg in self.registry.regs:
                if reg.name not in device.register:
                    dev.register(reg.callback, reg.condition, n=reg.n,
                                 millis=reg.millis, name=reg.name)

    def __getattr__(self, attr):
        return getattr(self.__module__, attr)

    def __iter__(self):
        for reg in registry:
            yield reg.name

    def __delitem__(self, item):
        del registry[item]

        for device in device_list:
            if item in device.register:
                del device.register

sys.modules[__name__] = Register(sys.modules[__name__])
