import pyudev

from . import udev_context, _3dconnexion_match


class Monitor(object):
    _udev_monitor = None

    def __init__(self):
        self._udev_monitor = pyudev.Monitor.from_netlink(udev_context)
        self._udev_monitor.filter_by('input')

    @property
    def fd(self):
        return self._udev_monitor.fileno()

    def fileno(self):
        return self._udev_monitor.fileno()

    def start(self):
        self._udev_monitor.start()

    def read_one(self, valid_only=True):
        if self._udev_monitor.started:
            for device in iter(self._udev_monitor.poll, None):
                match = _3dconnexion_match(device)

                if match is not None:
                    return device.action, match

                if not valid_only:
                    return None, (None, None, None)

    def read(self, valid_only=True):
        if self._udev_monitor.started:
            for device in iter(self._udev_monitor.poll, None):
                match = _3dconnexion_match(device)

                if match is not None:
                    yield device.action, match

                if not valid_only:
                    yield None, (None, None, None)
