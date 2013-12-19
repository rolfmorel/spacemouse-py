from __future__ import print_function

from .. import list_devices
from . import match_regex_options


def main(args):
    for mouse in list_devices():
        if not match_regex_options(mouse, args):
            continue

        with mouse:
            if args.action in (None, "switch", "!"):
                if args.action is not None:  # switch action
                    mouse.led = not mouse.led

                led_state = "on" if mouse.led else "off"

                if args.action is not None:
                    print("{0.devnode}: switched {1}".format(mouse, led_state))
                else:
                    print("{0.devnode}: {1}".format(mouse, led_state))
            else:
                new_state = True if args.action in ("on", "1") else False

                mouse.led = new_state
