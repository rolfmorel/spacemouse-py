#!/usr/bin/env python

from __future__ import print_function

import libspacemouse
from libspacemouse import SpaceMouseDeviceList, background
from libspacemouse.event import any_button_press


def button_press_cb(event, n, mouse, name):
    led_state = mouse.led = not mouse.led
    print(mouse, "switched led", "on" if led_state else "off")


def mouse_add_cb(mouse):
    print(mouse, "added")
    mouse.open()
    libspacemouse.register(button_press_cb, mouse, any_button_press, 1)


def mouse_remove_cb(mouse):
    print(mouse, "removed")
    del libspacemouse.register[mouse]
    mouse.close()


if __name__ == "__main__":
    libspacemouse.monitor(add=mouse_add_cb, remove=mouse_remove_cb)

    for mouse in SpaceMouseDeviceList():
        mouse.open()
        libspacemouse.register(button_press_cb, mouse, any_button_press, 1)

    background.run()
