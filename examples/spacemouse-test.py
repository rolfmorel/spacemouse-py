#!/usr/bin/env python

# A Python implementation of the spacemouse-test program from spacemouse-utils

import libspacemouse
from libspacemouse import reg_events, background


def motion_cb(event, n, mouse, name):
    print("device id {0.id}: ".format(mouse), end="")
    print("got motion event: t({0.x}, {0.y}, {0.z})"
          " r({0.rx}, {0.ry}, {0.rz}) period ({0.period})".format(event))


def button_cb(event, n, mouse, name):
    print("device id {0.id}: ".format(mouse), end="")
    action = "press" if event.press else "release"
    print("got button " + action + " event: b({0.bnum})".format(event))


def mouse_add_cb(mouse):
    print("Device added, device id: {0.id}\n"
          "  devnode: {0.devnode}\n"
          "  manufaturer: {0.manufacturer}\n"
          "  product: {0.product}".format(mouse))
    mouse.open()
    libspacemouse.register(motion_cb, mouse, reg_events.any_motion, 1)
    libspacemouse.register(button_cb, mouse, reg_events.any_button, 1)


def mouse_remove_cb(mouse):
    print("Device removed, device id: {0.id}\n"
          "  devnode: {0.devnode}\n"
          "  manufaturer: {0.manufacturer}\n"
          "  product: {0.product}".format(mouse))
    del libspacemouse.register[mouse]
    mouse.close()


if __name__ == "__main__":
    libspacemouse.monitor(add=mouse_add_cb, remove=mouse_remove_cb)

    for mouse in libspacemouse.spacemouse_device_list_update():
        print("device id: {0.id}\n"
              "  devnode: {0.devnode}\n"
              "  manufaturer: {0.manufacturer}\n"
              "  product: {0.product}".format(mouse))

        mouse.open()
        libspacemouse.register(motion_cb, mouse, reg_events.any_motion, 1)
        libspacemouse.register(button_cb, mouse, reg_events.any_button, 1)

    background.run()
