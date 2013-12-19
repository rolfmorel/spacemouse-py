from __future__ import print_function

from .. import MIN_DEVIATION, N_EVENTS
from .. import list_devices, event, register, monitor, loop
from . import match_regex_options

motions = ("right", "left",
           "back", "forward",
           "down", "up",
           "pitch back", "pitch forward",
           "roll left", "roll right",
           "yaw right", "yaw left")


def main(args):
    def motion_cb(event, n, name, mouse):
        print("motion:", name)

    def button_cb(event, n, name, mouse):
        print("button:", event.bnum, "press" if event.press else "release")

    def mouse_add_cb(mouse):
        if match_regex_options(mouse, args):
            print("device:", mouse.devnode, mouse.manufacturer, mouse.product,
                  "connect")

            mouse.open()

    def mouse_remove_cb(mouse):
        print("device:", mouse.devnode, mouse.manufacturer, mouse.product,
              "disconnect")

    MIN_DEVIATION = args.deviation

    monitor(add=mouse_add_cb, remove=mouse_remove_cb).start()

    for mouse in list_devices():
        if match_regex_options(mouse, args):
            mouse.open()

    if args.milliseconds > 0:
        n_events, millis = None, args.milliseconds
    else:
        n_events, millis = args.events, None

    for moiton_name in motions:
        reg_event = getattr(event, "motion_" + moiton_name.replace(" ", "_"))

        register(motion_cb, reg_event, n=n_events, millis=millis,
                 name=moiton_name)

    register(button_cb, event.any_button, n=1)

    try:
        loop.run()
    except KeyboardInterrupt:
        print()
