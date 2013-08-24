#!/usr/bin/env python2

import Xlib
import Xlib.display
from Xlib.XK import string_to_keysym
from Xlib.ext.xtest import fake_input

import libspacemouse
from libspacemouse import SpaceMouseDeviceList, background
from libspacemouse.reg_events import (motion_forward, motion_right,
                                      motion_back, motion_left,
                                      motion_pitch_forward, motion_pitch_back,
                                      motion_roll_left, motion_roll_right)

display = Xlib.display.Display()

string_to_keycode = lambda x: display.keysym_to_keycode(string_to_keysym(x))

name_to_event = {'forward': motion_forward, 'back': motion_back,
                 'left': motion_left, 'right': motion_right,
                 'pitch_forward': motion_pitch_forward,
                 'pitch_back': motion_pitch_back,
                 'roll_left': motion_roll_left,
                 'roll_right': motion_roll_right}

name_to_button = {'pitch_forward': 4, 'pitch_back': 5, 'roll_left': 6,
                  'roll_right': 7}

name_to_key = {'forward': string_to_keycode('Up'),
               'back': string_to_keycode('Down'),
               'left': string_to_keycode('Left'),
               'right': string_to_keycode('Right')}


def motion_cb(event, n, mouse, name):
    if name_to_button.get(name):
        fake_input(display, Xlib.X.ButtonPress, name_to_button[name])
        fake_input(display, Xlib.X.ButtonRelease, name_to_button[name])
    else:
        fake_input(display, Xlib.X.KeyPress, name_to_key[name])
        fake_input(display, Xlib.X.KeyRelease, name_to_key[name])
    display.sync()


def mouse_add_cb(mouse):
    mouse.open()

    for name, ev in name_to_event.iteritems():
        libspacemouse.register(motion_cb, mouse, ev, m_sec=96, name=name)


def mouse_remove_cb(mouse):
    del libspacemouse.register[mouse]
    mouse.close()


if __name__ == "__main__":
    libspacemouse.monitor(add=mouse_add_cb, remove=mouse_remove_cb)

    for mouse in SpaceMouseDeviceList().update():
        mouse.open()

        for name, ev in name_to_event.iteritems():
            libspacemouse.register(motion_cb, mouse, ev, m_sec=96, name=name)

    background.run()
