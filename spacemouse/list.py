from . import backend
from .device import Device

if backend.get('list') == "udev":
    from .udev.list import list_devices as backend_list_devices
else:
    raise ValueError("No valid 'list' backend specified")

device_list = []


def list_devices():
    for devnode, manufacturer, product in backend_list_devices():
        device = Device(devnode, manufacturer, product)

        if device not in device_list:
            device_list.append(device)

    return device_list
