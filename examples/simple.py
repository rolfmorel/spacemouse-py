#!/usr/bin/env python

from __future__ import print_function

from spacemouse import list_devices, monitor, loop
from spacemouse.event import (motion_forward, motion_right, motion_back,
                              motion_left, any_button)

name_event = { 'forward': motion_forward, 'right': motion_right,
               'back': motion_back, 'left': motion_left }


def motion_cb(event, n, name, mouse):
    print(mouse, "motion push", name)


def button_cb(event, n, name, mouse):
    action = "pressed" if event.press else "released"

    print(mouse, "button", event.bnum, action)


def mouse_add_cb(mouse):
    print(mouse, "added")

    mouse.open()

    mouse.register(button_cb, any_button, 1)
    for name, event in name_event.items():
        mouse.register(motion_cb, event, 16, name=name)


def mouse_remove_cb(mouse):
    print(mouse, "removed")

    mouse.close()


if __name__ == "__main__":
    monitor(add=mouse_add_cb, remove=mouse_remove_cb)
    monitor.start()

    for mouse in list_devices():
        mouse.open()

        mouse.register(button_cb, any_button, 1)
        for name, event in name_event.items():
            mouse.register(motion_cb, event, 16, name=name)

    loop.run()
