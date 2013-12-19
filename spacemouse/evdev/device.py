from errno import ENODEV

from evdev import InputDevice, ecodes

from ..event import MotionEvent, ButtonEvent, LedEvent


class Device(object):
    devnode = None

    _input_device = None
    _last_motion = None
    _last_timecode = [0, 0]

    def __init__(self, devnode, open=False):
        self.devnode = devnode

        if open:
            self.open()

    def __eq__(self, other):
        if self._input_device is None:
            return False
        if not hasattr(other, "_input_device"):
            return False

        return self._input_device == other._input_device

    def __del__(self):
        if self._input_device is not None and hasattr(self, 'close'):
            self.close()

    @property
    def fd(self):
        return self._input_device.fd if self._input_device is not None else -1

    @property
    def led(self):
        if self._input_device is not None:
            return bool(self._input_device.leds())

    @led.setter
    def led(self, state):
        if self._input_device is not None:
            return self._input_device.set_led(ecodes.LED_MISC, state)

    def fileno(self):
        if self._input_device is not None:
            return self._input_device.fileno()

        return -1

    def open(self):
        if self._input_device is None:
            self._input_device = InputDevice(self.devnode)
        else:
            raise RuntimeError("can not open an already opened device")

        return self.fd

    def close(self, silent=False):
        if self._input_device is not None:
            try:
                self._input_device.close()
            except OSError as err:
                if not (err.errno == ENODEV and silent):
                    raise
            finally:
                del self._input_device

                self._input_device = None
        else:
            raise RuntimeError("can not close an unopened device")

    def grab(self):
        if self._input_device is not None:
            return self._input_device.grab()

    def ungrab(self):
        if self._input_device is not None:
            return self._input_device.ungrab()

    def _convert(self, ev):
        event = None

        if ev.type in (ecodes.EV_ABS, ecodes.EV_REL):  # motion events
            if self._last_motion is None:
                self._last_motion = MotionEvent()

            event = self._last_motion

            if self._last_timecode[0] > 0:
                millis = (ev.sec - self._last_timecode[0]) * 1000
                millis += (ev.usec - self._last_timecode[1]) // 1000

                event.period = millis

            axis_map = {ecodes.ABS_X: 'x', ecodes.REL_X: 'x',
                        ecodes.ABS_Y: 'y', ecodes.REL_Y: 'y',
                        ecodes.ABS_Z: 'z', ecodes.REL_Z: 'z',
                        ecodes.ABS_RX: 'rx', ecodes.REL_RX: 'rx',
                        ecodes.ABS_RY: 'ry', ecodes.REL_RY: 'ry',
                        ecodes.ABS_RZ: 'rz', ecodes.REL_RZ: 'rz'
                        }

            setattr(event, axis_map[ev.code], ev.value)
        elif ev.type == ecodes.EV_KEY:
            event = ButtonEvent()

            event.bnum = ev.code - ecodes.BTN_0
            event.press = ev.value
        elif ev.type == ecodes.EV_LED and ev.code == ecodes.LED_MISC:
            event = LedEvent()

            event.state = ev.value

        return ev.type, event

    def read_one(self):
        if self._input_device is None:
            return

        prev_event = None

        for ev in self._input_device.read_loop():
            ev_type, event = self._convert(ev)

            if event:
                prev_event = event
            if ev_type == ecodes.EV_SYN and prev_event:
                if type(prev_event) == MotionEvent:
                    self._last_timecode = ev.sec, ev.usec

                break

        return prev_event

    def read(self):
        if self._input_device is None:
            return

        prev_event = None

        for ev in self._input_device.read_loop():
            ev_type, event = self._convert(ev)

            if event:
                prev_event = event
            if ev_type == ecodes.EV_SYN and prev_event:
                if type(prev_event) == MotionEvent:
                    self._last_timecode = ev.sec, ev.usec

                yield prev_event
