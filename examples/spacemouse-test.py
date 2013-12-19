#!/usr/bin/env python

# A Python implementation of the 'raw' command of 'spm' from spacemouse

from __future__ import print_function

from spacemouse import list_devices, monitor, loop, register, event


def motion_cb(event, n, name, mouse):
    print("device id {0.id}: ".format(mouse), end="")
    print("got motion event: t({0.x}, {0.y}, {0.z})"
          " r({0.rx}, {0.ry}, {0.rz}) period ({0.period})".format(event))


def button_cb(event, n, name, mouse):
    print("device id {0.id}: ".format(mouse), end="")

    action = "press" if event.press else "release"
    print("got button " + action + " event: b({0.bnum})".format(event))


def mouse_add_cb(mouse):
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


if __name__ == "__main__":
    monitor(add=mouse_add_cb, remove=mouse_remove_cb)
    monitor.start()

    for mouse in list_devices():
        print("device id: {0.id}\n"
              "  devnode: {0.devnode}\n"
              "  manufaturer: {0.manufacturer}\n"
              "  product: {0.product}".format(mouse))

        mouse.open()

    register(motion_cb, event.any_motion, 1)
    register(button_cb, event.any_button, 1)

    loop.run()
