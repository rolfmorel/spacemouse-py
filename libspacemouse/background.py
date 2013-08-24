import select
try:
    import threading
except ImportError:
    import dummy_threading as threading

from time import sleep

from . import register
from . import monitor
from .wrapper import (spacemouse_device_read_event, spacemouse_monitor,
                      ACTIONS, READS)

background_thread = None


def run(timeout=0.2, ref=None):
    while True:
        if ref and ref._stop_event.is_set():
            break
        rfds = []

        if monitor.monitor_fd > -1:
            rfds.append(monitor.monitor_fd)

        for reg_mouse in register.registered_mouses:
            if reg_mouse.mouse.fd > -1:
                rfds.append(reg_mouse.mouse.fd)

        if len(rfds) == 0:
            sleep(timeout)
            continue

        sel_rfds, _, _ = select.select(rfds, [], [], timeout)

        if len(sel_rfds) == 0:
            continue

        for fd in sel_rfds:
            if fd == monitor.monitor_fd:
                action, mouse = spacemouse_monitor()

                if (action == ACTIONS['SPACEMOUSE_ACTION_ADD'] and
                        monitor.monitor_add_callback is not None):
                    monitor.monitor_add_callback(mouse)
                elif (action == ACTIONS['SPACEMOUSE_ACTION_REMOVE'] and
                      monitor.monitor_remove_callback is not None):
                    monitor.monitor_remove_callback(mouse)
                continue

            for reg_mouse in register.registered_mouses:
                if reg_mouse.mouse.fd == fd:
                    ret, event = spacemouse_device_read_event(reg_mouse.mouse)
                    if ret == READS['SPACEMOUSE_READ_SUCCESS']:
                        register.parse_event(event, reg_mouse)
                    break


class BackgroundThread(threading.Thread):
    daemon = True

    def __init__(self):
        super(BackgroundThread, self).__init__()
        self._stop_event = threading.Event()
        self.start()

    def run(self):
        global background_thread

        background_thread = self

        run(ref=self)

    def stop(self):
        global background_thread

        self._stop_event.set()
        self.join()

        background_thread = None
