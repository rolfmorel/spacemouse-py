from __future__ import print_function

from .. import list_devices
from . import match_regex_options


def main(args):
    msg = ("devnode: {0.devnode}\n"
           "manufacturer: {0.manufacturer}\n"
           "product: {0.product}\n")

    for mouse in list_devices():
        if match_regex_options(mouse, args):
            print(msg.format(mouse))
