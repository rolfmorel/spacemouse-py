import sys

from types import ModuleType


class RegisterMouse(object):
    cb_cond = {}
    # cb_cond = \
    # { callback_name:
    #      (callback, requisite_event, n_times_condition, millisecond_condtion)
    #  }
    cond_state = {}
    # cond_state = \
    # { callback_name:
    #      [n_times_state, millisecond_past_state, millisecond_n_consecutive]
    # }

    def __init__(self, mouse):
        self.mouse = mouse


registered_mouses = []


def parse_reg_event(reg_event, event):
    ret = None
    for event_type, desc in reg_event.items():
        if not isinstance(event, event_type):
            return False
        elif not isinstance(desc, dict):
            return True
        for attr, cond in desc.items():
            func, args = cond['function'], cond['arguments']
            if func(getattr(event, attr), *args):
                ret = True
            else:
                return False
    return ret


def parse_event(event, reg_mouse):
    for name, (cb, reg, n_event, m_sec) in reg_mouse.cb_cond.items():
        if parse_reg_event(reg, event):
            if m_sec:
                reg_mouse.cond_state[name][1] += event.period
                if reg_mouse.cond_state[name][1] > m_sec:
                    reg_mouse.cond_state[name][1] %= m_sec

                    cb(event, reg_mouse.cond_state[name][2], reg_mouse.mouse,
                       name)
                    reg_mouse.cond_state[name][2] += 1
            else:
                reg_mouse.cond_state[name][0] += 1
                if reg_mouse.cond_state[name][0] % n_event == 0:
                    cb(event, int(reg_mouse.cond_state[name][0] / n_event) - 1,
                       reg_mouse.mouse, name)
        else:
            reg_mouse.cond_state[name] = [0, 0, 0]


class Register(ModuleType):
    def __init__(self, module):
        self.__module__ = module
        self.__name__ = module.__name__

    def __call__(self, callback, mouse, reg_event, n=None, m_sec=None,
                 name=None, thread=None):
        global registered_mouses

        if not callable(callback):
            raise TypeError("callback argument must be callable")
        if n is None and m_sec is None:
            raise ValueError("either n argument or m_sec argument needed")
        elif n is not None and m_sec is not None:
            raise ValueError("either n argument or m_sec argument needed, "
                             "not both")

        name = name or callback.__name__
        for reg_mouse in registered_mouses:
            if reg_mouse.mouse == mouse:
                reg_mouse.cb_cond[name] = (callback, reg_event, n, m_sec)
                reg_mouse.cond_state[name] = [0, 0, 0]
                break
        else:
            reg_mouse = RegisterMouse(mouse)
            reg_mouse.cb_cond[name] = (callback, reg_event, n, m_sec)
            reg_mouse.cond_state[name] = [0, 0, 0]
            registered_mouses.append(reg_mouse)

        if thread is not None:
            from .background import background_thread, BackgroundThread
            if background_thread is None:
                thread = BackgroundThread()
            else:
                thread = background_thread
        return thread

    def __getattr__(self, attr):
        return getattr(self.__module__, attr)

    def __getitem__(self, item):
        for reg_mouse in registered_mouses:
            if reg_mouse.mouse == item:
                return reg_mouse.cb_cond
        raise KeyError(item)

    def __delitem__(self, item):
        for n, reg_mouse in enumerate(registered_mouses):
            if reg_mouse.mouse == item:
                del registered_mouses[n]
                return
        raise KeyError(item)

    def __iter__(self):
        for mouse, _, _ in registered_mouses:
            yield mouse


sys.modules[__name__] = Register(sys.modules[__name__])
