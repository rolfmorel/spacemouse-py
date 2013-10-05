from . import MIN_DEVIATION, AXIS_MAP_SPACENAVD

EVENTS = {'SPACEMOUSE_EVENT_MOTION': 1,
          'SPACEMOUSE_EVENT_BUTTON': 2,
          'SPACEMOUSE_EVENT_LED': 4
          }


class SpaceMouseEvent(object):
    type = -1

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SpaceMouseMotionEvent(SpaceMouseEvent):
    type = EVENTS['SPACEMOUSE_EVENT_MOTION']

    x, y, z = 0, 0, 0
    rx, ry, rz = 0, 0, 0
    period = 0


class SpaceMouseButtonEvent(SpaceMouseEvent):
    type = EVENTS['SPACEMOUSE_EVENT_BUTTON']

    press = 0
    bnum = 0


class SpaceMouseLedEvent(SpaceMouseEvent):
    type = EVENTS['SPACEMOUSE_EVENT_LED']

    state = 0


class RegisterEvent(object):
    ev_types = (SpaceMouseMotionEvent, SpaceMouseButtonEvent,
                SpaceMouseLedEvent)

    def __init__(self, **kwargs):
        for kw, val in kwargs.items():
            setattr(self, kw, val)

    def __call__(self, event):
        if not type(event) in self.ev_types:
            return False

        attrs = (attr for attr in dir(event) if (not attr.startswith('_') and
                                                 hasattr(self, attr)))

        for attr in attrs:
            call = getattr(self, attr)
            if not call(getattr(event, attr)):
                return False

        return True


class MotionRegisterEvent(RegisterEvent):
    ev_types = (SpaceMouseMotionEvent,)


class ButtonRegisterEvent(RegisterEvent):
    ev_types = (SpaceMouseButtonEvent,)


class LedRegisterEvent(RegisterEvent):
    ev_types = (SpaceMouseLedEvent,)


any_motion = MotionRegisterEvent()

no_motion = MotionRegisterEvent()
for attr in ('x', 'y', 'z', 'rx', 'ry', 'rz'):
    setattr(no_motion, attr, lambda a: -MIN_DEVIATION <= a <= MIN_DEVIATION)

axis_x_pos = MotionRegisterEvent(x=lambda a: a > MIN_DEVIATION)
axis_x_neg = MotionRegisterEvent(x=lambda a: a < -MIN_DEVIATION)

axis_y_pos = MotionRegisterEvent(y=lambda a: a > MIN_DEVIATION)
axis_y_neg = MotionRegisterEvent(y=lambda a: a < -MIN_DEVIATION)

axis_z_pos = MotionRegisterEvent(z=lambda a: a > MIN_DEVIATION)
axis_z_neg = MotionRegisterEvent(z=lambda a: a < -MIN_DEVIATION)

axis_rx_pos = MotionRegisterEvent(rx=lambda a: a > MIN_DEVIATION)
axis_rx_neg = MotionRegisterEvent(rx=lambda a: a < -MIN_DEVIATION)

axis_ry_pos = MotionRegisterEvent(ry=lambda a: a > MIN_DEVIATION)
axis_ry_neg = MotionRegisterEvent(ry=lambda a: a < -MIN_DEVIATION)

axis_rz_pos = MotionRegisterEvent(rz=lambda a: a > MIN_DEVIATION)
axis_rz_neg = MotionRegisterEvent(rz=lambda a: a < -MIN_DEVIATION)

any_button = ButtonRegisterEvent()

any_button_press = ButtonRegisterEvent(press=lambda a: bool(a))

button0 = ButtonRegisterEvent(bnum=lambda a: a == 0)
button1 = ButtonRegisterEvent(bnum=lambda a: a == 1)

not_button0_or_1 = ButtonRegisterEvent(bnum=lambda a: a > 1)

led = LedRegisterEvent()
led_on = LedRegisterEvent(state=lambda a: bool(a))
led_off = LedRegisterEvent(state=lambda a: not bool(a))

motion_right = axis_x_pos
motion_left = axis_x_neg
motion_up = axis_y_pos if AXIS_MAP_SPACENAVD else axis_z_neg
motion_down = axis_y_neg if AXIS_MAP_SPACENAVD else axis_z_pos
motion_forward = axis_z_pos if AXIS_MAP_SPACENAVD else axis_y_neg
motion_back = axis_z_neg if AXIS_MAP_SPACENAVD else axis_y_pos
motion_pitch_forward = axis_rx_neg
motion_pitch_back = axis_rx_pos
motion_yaw_left = axis_ry_pos if AXIS_MAP_SPACENAVD else axis_rz_neg
motion_yaw_right = axis_ry_neg if AXIS_MAP_SPACENAVD else axis_rz_pos
motion_roll_right = axis_rz_pos if AXIS_MAP_SPACENAVD else axis_ry_neg
motion_roll_left = axis_rz_neg if AXIS_MAP_SPACENAVD else axis_ry_pos
