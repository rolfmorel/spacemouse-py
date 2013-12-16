#!/usr/bin/env python

from __future__ import print_function

from spacemouse import list_devices, monitor, loop
from spacemouse.event import any_button_press


def button_press_cb(event, n, name, mouse):
    led_state = mouse.led = not mouse.led

    print(mouse, "led switched", "on" if led_state else "off")


def mouse_add_cb(mouse):
    print(mouse, "added")

    mouse.open()
    mouse.register(button_press_cb, any_button_press, 1)


def mouse_remove_cb(mouse):
    print(mouse, "removed")

    mouse.close()


if __name__ == "__main__":
    monitor(add=mouse_add_cb, remove=mouse_remove_cb)

    for mouse in list_devices():
        mouse.open()
        mouse.register(button_press_cb, any_button_press, 1)

    loop.run()
