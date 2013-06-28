from ctypes import cdll, c_int, c_char_p, byref, POINTER

from .structure import spacemouse, spacemouse_event

__all__ = ('EVENTS', 'ACTIONS', 'READS', 'SpaceMouse', 'SpaceMouseEvent',
           'SpaceMouseEventMotion', 'SpaceMouseEventButton',
           'spacemouse_device_list', 'spacemouse_device_list_update',
           'spacemouse_monitor_open', 'spacemouse_monitor',
           'spacemouse_monitor_close', 'spacemouse_device_open',
           'spacemouse_device_grab', 'spacemouse_device_ungrab',
           'spacemouse_device_read_event', 'spacemouse_device_get_led',
           'spacemouse_device_set_led', 'spacemouse_monitor_close')

libspacemouse = cdll.LoadLibrary("libspacemouse.so")

libspacemouse.spacemouse_device_list.restype = POINTER(spacemouse)
libspacemouse.spacemouse_device_list_update.restype = POINTER(spacemouse)
libspacemouse.spacemouse_device_list_get_next.restype = POINTER(spacemouse)

libspacemouse.spacemouse_monitor.restype = POINTER(spacemouse)

libspacemouse.spacemouse_device_get_devnode.restype = c_char_p
libspacemouse.spacemouse_device_get_manufacturer.restype = c_char_p
libspacemouse.spacemouse_device_get_product.restype = c_char_p

EVENTS = ['SPACEMOUSE_EVENT_ANY',
          'SPACEMOUSE_EVENT_MOTION',
          'SPACEMOUSE_EVENT_BUTTON']

ACTIONS = ['SPACEMOUSE_ACTION_IGNORE',
           'SPACEMOUSE_ACTION_ADD',
           'SPACEMOUSE_ACTION_REMOVE',
           'SPACEMOUSE_ACTION_CHANGE',
           'SPACEMOUSE_ACTION_ONLINE',
           'SPACEMOUSE_ACTION_OFFLINE']

READS = ['SPACEMOUSE_READ_IGNORE',
         'SPACEMOUSE_READ_SUCCESS']


#TODO: decide if this is even a good idea to add
class SpaceMouseDeviceList(list):
    def __getslice__(self, i, j):
        return SpaceMouseDeviceList(list.__getslice__(self, i, j))

    def __add__(self, other):
        return SpaceMouseDeviceList(list.__add__(self, other))

    def __mul__(self, other):
        return SpaceMouseDeviceList(list.__mul__(self, other))

    def update(self):
        return _spacemouse_device_list(
            libspacemouse.spacemouse_device_list_update, type(self))


class SpaceMouseEvent(object):
    type = EVENTS.index('SPACEMOUSE_EVENT_ANY')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SpaceMouseEventMotion(SpaceMouseEvent):
    type = EVENTS.index('SPACEMOUSE_EVENT_MOTION')

    x, y, z = 0, 0, 0
    rx, ry, rz = 0, 0, 0
    period = 0


class SpaceMouseEventButton(SpaceMouseEvent):
    type = EVENTS.index('SPACEMOUSE_EVENT_BUTTON')

    press = 0
    bnum = 0


class SpaceMouse(object):
    def __init__(self, ptr):
        self.id = libspacemouse.spacemouse_device_get_id(ptr)
        self.fd = libspacemouse.spacemouse_device_get_fd(ptr)
        self.devnode = \
            libspacemouse.spacemouse_device_get_devnode(ptr).decode()
        self.manufacturer = \
            libspacemouse.spacemouse_device_get_manufacturer(ptr).decode()
        self.product = \
            libspacemouse.spacemouse_device_get_product(ptr).decode()
        self._pointer = ptr

    def __eq__(self, other):
        return self.id == other.id and self.devnode == other.devnode

    def __str__(self):
        return "{0.manufacturer} {0.product}".format(self)

    def fileno(self):
        return self.fd

    @property
    def led(self):
        return bool(spacemouse_device_get_led(self))

    @led.setter
    def led(self, state):
        spacemouse_device_set_led(self, int(state))

    def open(self):
        return spacemouse_device_open(self)

    def close(self):
        return spacemouse_device_close(self)

    def grab(self):
        return spacemouse_device_grab(self)

    def ungrab(self):
        return spacemouse_device_ungrab(self)

    def read_event(self):
        event_ret, event = READS.index('SPACEMOUSE_READ_IGNORE'), None
        while event_ret == READS.index('SPACEMOUSE_READ_IGNORE'):
            event_ret, event = spacemouse_device_read_event(self)
        return event

# For use with the C wrapper API
spacemouse_list = []

#TODO: decide if this is even a good idea to add
# For use with OO python API
device_list = SpaceMouseDeviceList()


#TODO: decide if this is even a good idea to add list_type stuff
def _spacemouse_device_list(func, list_type=None):
    global spacemouse_list

    ptr = func()
    if list_type:
        ret_list = list_type()
    else:
        ret_list = spacemouse_list = []
    while bool(ptr):
        mouse = SpaceMouse(ptr)

        ret_list.append(mouse)
        ptr = libspacemouse.spacemouse_device_list_get_next(ptr)
    return ret_list


def spacemouse_device_list():
    return _spacemouse_device_list(libspacemouse.spacemouse_device_list)


def spacemouse_device_list_update():
    return _spacemouse_device_list(libspacemouse.spacemouse_device_list_update)


def spacemouse_monitor_open():
    return libspacemouse.spacemouse_monitor_open()


def spacemouse_monitor():
    global spacemouse_list

    action = c_int()
    mouse = None

    ptr = libspacemouse.spacemouse_monitor(byref(action))

    if ptr and (action.value == ACTIONS.index('SPACEMOUSE_ACTION_ADD') or
                action.value == ACTIONS.index('SPACEMOUSE_ACTION_REMOVE')):

        mouse = SpaceMouse(ptr)

        if action.value == ACTIONS.index('SPACEMOUSE_ACTION_ADD'):
            spacemouse_list.append(mouse)
        else:
            for m in spacemouse_list:
                if m == mouse:
                    spacemouse_list.remove(m)

    return action.value, mouse


def spacemouse_monitor_close():
    return libspacemouse.spacemouse_monitor_close()


def spacemouse_device_open(mouse):
    fd = libspacemouse.spacemouse_device_open(mouse._pointer)
    if fd > -1:
        mouse.fd = fd
        for m in spacemouse_list:
            if m == mouse:
                m.fd = mouse.fd
    return fd


def spacemouse_device_grab(mouse):
    return libspacemouse.spacemouse_device_grab(mouse._pointer)


def spacemouse_device_ungrab(mouse):
    return libspacemouse.spacemouse_device_ungrab(mouse._pointer)


def spacemouse_device_read_event(mouse):
    ev = spacemouse_event()
    event = None

    ret = libspacemouse.spacemouse_device_read_event(mouse._pointer, byref(ev))

    if ret == READS.index('SPACEMOUSE_READ_SUCCESS'):
        if ev.type == EVENTS.index('SPACEMOUSE_EVENT_MOTION'):
            event = SpaceMouseEventMotion()
            event.x, event.y, event.z = ev.motion.x, ev.motion.y, ev.motion.z
            event.rx, event.ry = ev.motion.rx, ev.motion.ry
            event.rz = ev.motion.rz
            event.period = ev.motion.period
        elif ev.type == EVENTS.index('SPACEMOUSE_EVENT_BUTTON'):
            event = SpaceMouseEventButton()
            event.press = ev.button.press
            event.bnum = ev.button.bnum
    return ret, event


def spacemouse_device_get_led(mouse):
    return libspacemouse.spacemouse_device_get_led(mouse._pointer)


def spacemouse_device_set_led(mouse, state):
    return libspacemouse.spacemouse_device_set_led(mouse._pointer,
                                                   c_int(state))


def spacemouse_device_close(mouse):
    ret = libspacemouse.spacemouse_device_close(mouse._pointer)

    if ret == 0:
        mouse.fd = -1
        for m in spacemouse_list:
            if m == mouse:
                m.fd = mouse.fd
    return ret
