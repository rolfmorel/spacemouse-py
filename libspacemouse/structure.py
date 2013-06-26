from ctypes import c_int, c_uint, Structure, Union


class spacemouse(Structure):
    pass


class spacemouse_event_motion(Structure):
    _fields_ = [('type', c_int),
                ('x', c_int),
                ('y', c_int),
                ('z', c_int),
                ('rx', c_int),
                ('ry', c_int),
                ('rz', c_int),
                ('period', c_uint)]


class spacemouse_event_button(Structure):
    _fields_ = [('type', c_int),
                ('press', c_int),
                ('bnum', c_int)]


class spacemouse_event(Union):
    _fields_ = [('type', c_int),
                ('motion', spacemouse_event_motion),
                ('button', spacemouse_event_button)]
