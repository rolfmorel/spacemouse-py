import os
import select
from collections import namedtuple
from errno import ENODEV

try:
    from threading import Thread
except ImportError:
    from dummy_threading import Thread

from . import monitor
from .list import device_list

Pipe = namedtuple('Pipe', ('source', 'sink'))

stop_pipe = Pipe(-1, -1)


def run(thread=None):
    if thread:
        global stop_pipe

        stop_pipe = Pipe(*os.pipe())

        name = thread if thread is not True else None
        return Thread(target=run, name=name)

    while True:
        rlist = []

        if stop_pipe.source > -1:
            rlist.append(stop_fd)

        if monitor.fd > -1:
            rlist.append(monitor.fd)

        for device in device_list:
            if device.fd > -1:
                rlist.append(device.fd)

        rfds, _, _ = select.select(rlist, [], [])

        for fd in rfds:
            if fd == stop_pipe.source:
                os.close(stop_pipe.source)
                os.close(stop_pipe.sink)

                stop_pipe = Pipe(-1, -1)

                return

            if fd == monitor.fd:
                monitor.dispatch()

                continue

            for device in device_list:
                if fd == device.fd:
                    try:
                        event = device.read_one()
                    except IOError as err:
                        if err.errno == ENODEV:
                            device.close(silent=True)
                        else:
                            raise
                    else:
                        device.register.dispatch(event, device)

                    break


def stop():
    if stop_pipe.sink > -1:
        os.write(stop_pipe.sink, "Stop!!!")
