from . import backend
from .device import Device, match_device

if backend.get('list') == "udev":
    from .udev.list import list_devices as backend_list_devices
else:
    raise ValueError("No valid 'list' backend specified")

device_list = []


def list_devices():
    for devnode, manufacturer, product in backend_list_devices():
        for device in device_list:
            if match_device(device, devnode, manufacturer, product):
                break
        else:
            device_list.append(Device(devnode, manufacturer, product))

    return device_list
