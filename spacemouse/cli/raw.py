from __future__ import print_function

from .. import list_devices, monitor, loop, register, event
from . import match_regex_options


def main(args):
    def motion_cb(event, n, name, mouse):
        print("device id {0.id}: ".format(mouse), end="")
        print("got motion event: t({0.x}, {0.y}, {0.z})"
              " r({0.rx}, {0.ry}, {0.rz}) period ({0.period})".format(event))

    def button_cb(event, n, name, mouse):
        print("device id {0.id}: ".format(mouse), end="")

        action = "press" if event.press else "release"
        print("got button " + action + " event: b({0.bnum})".format(event))

    def mouse_add_cb(mouse):
        if match_regex_options(mouse, args):
            print("Device added, device id: {0.id}\n"
                  "  devnode: {0.devnode}\n"
                  "  manufaturer: {0.manufacturer}\n"
                  "  product: {0.product}".format(mouse))

            mouse.open()

    def mouse_remove_cb(mouse):
        print("Device removed, device id: {0.id}\n"
              "  devnode: {0.devnode}\n"
              "  manufaturer: {0.manufacturer}\n"
              "  product: {0.product}".format(mouse))

    monitor(add=mouse_add_cb, remove=mouse_remove_cb).start()

    for mouse in list_devices():
        if match_regex_options(mouse, args):
            print("device id: {0.id}\n"
                  "  devnode: {0.devnode}\n"
                  "  manufaturer: {0.manufacturer}\n"
                  "  product: {0.product}".format(mouse))

            mouse.open()

    register(motion_cb, event.any_motion, 1)
    register(button_cb, event.any_button, 1)

    try:
        loop.run()
    except KeyboardInterrupt:
        print()
