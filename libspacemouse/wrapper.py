from ctypes import cdll, c_int, c_char_p, byref, POINTER

from .structure import spacemouse, spacemouse_event_t

_clib = cdll.LoadLibrary("libspacemouse.so")

_clib.spacemouse_device_list_get_next.restype = POINTER(spacemouse)


EVENTS = {'SPACEMOUSE_EVENT_MOTION': 1,
          'SPACEMOUSE_EVENT_BUTTON': 2,
          'SPACEMOUSE_EVENT_LED': 4
          }
_clib.spacemouse_device_get_devnode.restype = c_char_p
_clib.spacemouse_device_get_manufacturer.restype = c_char_p
_clib.spacemouse_device_get_product.restype = c_char_p

ACTIONS = {'SPACEMOUSE_ACTION_IGNORE': 0,
           'SPACEMOUSE_ACTION_ADD': 1,
           'SPACEMOUSE_ACTION_REMOVE': 2
           }

READS = {'SPACEMOUSE_READ_IGNORE': 0,
         'SPACEMOUSE_READ_SUCCESS': 1
         }

# For use with the C wrapper API
spacemouse_list = []


class SpaceMouseDeviceList(list):
    def __init__(self, *args, **kwargs):
        # 'update' is keyword only arg
        update = kwargs.pop('update', True)
        list.__init__(self, *args, **kwargs)

        if update:
            self.update()

    def __getslice__(self, i, j):
        return type(self)(list.__getslice__(self, i, j), update=False)

    def __add__(self, other):
        return type(self)(list.__add__(self, other), update=False)

    def __mul__(self, other):
        return type(self)(list.__mul__(self, other), update=False)

    def update(self):
        err, mouse_list = spacemouse_device_list(update=True)
        del self[:]
        for mouse in mouse_list:
            self.append(mouse)
        return self


class SpaceMouse(object):
    _max_axis_deviation = None

    def __init__(self, ptr):
        self.id = _clib.spacemouse_device_get_id(ptr)
        self.fd = _clib.spacemouse_device_get_fd(ptr)
        self.devnode = _clib.spacemouse_device_get_devnode(ptr).decode()
        self.manufacturer = \
            _clib.spacemouse_device_get_manufacturer(ptr).decode()
        self.product = _clib.spacemouse_device_get_product(ptr).decode()
        self._pointer = ptr

    def __eq__(self, other):
        return self.id == other.id and self.devnode == other.devnode

    def __str__(self):
        return "{0.manufacturer} {0.product}".format(self)

    def fileno(self):
        return self.fd

    @property
    def max_axis_deviation(self):
        if self._max_axis_deviation is None:
            self._max_axis_deviation = \
                spacemouse_device_get_max_axis_deviation(self)
        return self._max_axis_deviation

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

    def grab(self, grab=1):
        return spacemouse_device_set_grab(self, grab)

    def read_event(self):
        event_ret, event = READS['SPACEMOUSE_READ_IGNORE'], None
        while event_ret == READS['SPACEMOUSE_READ_IGNORE']:
            event_ret, event = spacemouse_device_read_event(self)
        return event


def spacemouse_device_list(update=None):
    global spacemouse_list

    update = 1 if update in (True, 1) else 0
    mouse_ptr = POINTER(spacemouse)()

    err = _clib.spacemouse_device_list(byref(mouse_ptr), c_int(update))

    if err == 0:
        spacemouse_list = []
        while bool(mouse_ptr):
            mouse = SpaceMouse(mouse_ptr)

            spacemouse_list.append(mouse)
            mouse_ptr = _clib.spacemouse_device_list_get_next(mouse_ptr)

    return err, spacemouse_list


def spacemouse_monitor_open():
    return _clib.spacemouse_monitor_open()


def spacemouse_monitor():
    global spacemouse_list

    mouse = None

    mouse_ptr = POINTER(spacemouse)()

    action = _clib.spacemouse_monitor(byref(mouse_ptr))

    if action in (ACTIONS['SPACEMOUSE_ACTION_ADD'],
                  ACTIONS['SPACEMOUSE_ACTION_REMOVE']) and mouse_ptr:
        mouse = SpaceMouse(mouse_ptr)

        if action == ACTIONS['SPACEMOUSE_ACTION_ADD']:
            spacemouse_list.append(mouse)
        else:
            for m in spacemouse_list:
                if m == mouse:
                    spacemouse_list.remove(m)

    return action, mouse


def spacemouse_monitor_close():
    return _clib.spacemouse_monitor_close()


def spacemouse_device_open(mouse):
    fd = _clib.spacemouse_device_open(mouse._pointer)
    if fd > -1:
        mouse.fd = fd
        for m in spacemouse_list:
            if m == mouse:
                m.fd = mouse.fd
    return fd


def spacemouse_device_get_max_axis_deviation(mouse):
    return _clib.spacemouse_device_get_max_axis_deviation(mouse._pointer)


def spacemouse_device_set_grab(mouse, grab):
    return _clib.spacemouse_device_set_grab(mouse._pointer, c_int(grab))


def spacemouse_device_read_event(mouse):
    ev = spacemouse_event_t()
    event = None

    ret = _clib.spacemouse_device_read_event(mouse._pointer, byref(ev))

    if ret == READS['SPACEMOUSE_READ_SUCCESS']:
        if ev.type == EVENTS['SPACEMOUSE_EVENT_MOTION']:
            event = SpaceMouseEventMotion()
            event.x, event.y, event.z = ev.motion.x, ev.motion.y, ev.motion.z
            event.rx, event.ry = ev.motion.rx, ev.motion.ry
            event.rz = ev.motion.rz
            event.period = ev.motion.period
        elif ev.type == EVENTS['SPACEMOUSE_EVENT_BUTTON']:
            event = SpaceMouseEventButton()
            event.press = ev.button.press
            event.bnum = ev.button.bnum
        elif ev.type == EVENTS['SPACEMOUSE_EVENT_LED']:
            event = SpaceMouseEventLed()
            event.state = ev.led.state
    return ret, event


def spacemouse_device_get_led(mouse):
    return _clib.spacemouse_device_get_led(mouse._pointer)


def spacemouse_device_set_led(mouse, state):
    return _clib.spacemouse_device_set_led(mouse._pointer, c_int(state))


def spacemouse_device_close(mouse):
    ret = _clib.spacemouse_device_close(mouse._pointer)

    if ret == 0:
        mouse.fd = -1
        for m in spacemouse_list:
            if m == mouse:
                m.fd = mouse.fd
    return ret
