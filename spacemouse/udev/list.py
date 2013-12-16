import pyudev

from . import udev_context, _3dconnexion_match


def list_devices():
    for device in udev_context.list_devices(subsystem='input'):
        match = _3dconnexion_match(device)

        if match is not None:
            yield match[0], match[1], match[2]
