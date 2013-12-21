from . import backend
from .registry import Registry

if backend.get('device') == "evdev":
    from .evdev.device import Device as BackendDevice
else:
    raise ValueError("No valid 'device' backend specified")

new_id = 1


def match_device(device, devnode, manufacturer, product):
    return ((device.devnode, device.manufacturer, device.product) ==
            (devnode, manufacturer, product))


class Device(BackendDevice):
    id = -1

    def __init__(self, devnode, manufacturer=None, product=None, open=False):
        global new_id

        super(Device, self).__init__(devnode, open)

        self.manufacturer = manufacturer or ""
        self.product = product or ""

        self.register = Registry()

        self.id = new_id

        new_id += 1

        if open:
            super(Device, self).open()

    def __eq__(self, other):
        for attr in ('devnode', 'manufacturer', 'product'):
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __str__(self):
        return "{0.manufacturer} {0.product}".format(self)

    def __repr__(self):
        msg = "{0}('{1.devnode}', '{1.manufacturer}', '{1.product}')"

        return msg.format(self.__class__.__name__, self)
