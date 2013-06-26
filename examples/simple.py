#!/usr/bin/env python

import libspacemouse
from libspacemouse import background
from libspacemouse.reg_events import (motion_forward, motion_right,
                                      motion_back, motion_left, any_button)


def motion_cb(event, n, mouse, name):
    print(mouse, "motion push", name)


def button_cb(event, n, mouse, name):
    action = "pressed" if event.press else "released"
    print(mouse, "button", event.bnum, action)


def mouse_add_cb(mouse):
    print(mouse, "added")
    mouse.open()
    libspacemouse.register(button_cb, mouse, any_button, 1)
    for ev, name in ((motion_forward, 'forward'), (motion_right, 'right'),
                     (motion_back, 'back'), (motion_left, 'left')):
        libspacemouse.register(motion_cb, mouse, ev, 16, name=name)


def mouse_remove_cb(mouse):
    print(mouse, "removed")
    del libspacemouse.register[mouse]
    mouse.close()


if __name__ == "__main__":
    libspacemouse.monitor(add=mouse_add_cb, remove=mouse_remove_cb)

    for mouse in libspacemouse.spacemouse_device_list_update():
        mouse.open()
        libspacemouse.register(button_cb, mouse, any_button, 1)
        for ev, name in ((motion_forward, 'forward'), (motion_right, 'right'),
                         (motion_back, 'back'), (motion_left, 'left')):
            libspacemouse.register(motion_cb, mouse, ev, 16, name=name)

    # Actually runs in current thread, functionality for loop is in background
    # module, use background.BackgroundThread() to run in seperate thread.
    background.run()
