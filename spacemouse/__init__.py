MIN_DEVIATION = 256
N_EVENTS = 16

# Default backends for linux
backend = {'list': "udev",
           'device': "evdev",
           'monitor': "udev"
           }


def list_devices():
    # import within function scope in case backend is changed before hand
    from .list import list_devices as list_devices_

    return list_devices_()
