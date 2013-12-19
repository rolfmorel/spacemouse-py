class RegStateN(object):
    n = 0


class RegStateMillis(object):
    millis_cur = 0
    consecutive = 0


class Reg(object):
    n = None
    millis = None

    def __init__(self, callback, condition, n=None, millis=None, name=None):
        if not callable(callback):
            raise TypeError("'callback' argument must be callable")

        if not callable(condition):
            raise TypeError("'condition' argument must be callable")

        self.name = name or callback.__name__
        self.callback = callback
        self.condition = condition

        if n and millis is None:
            self.n = int(n)
            self.state = RegStateN()
        elif millis and n is None:
            self.millis = int(millis)
            self.state = RegStateMillis()
        else:
            raise ValueError("either 'n' argument or 'millis' argument needed")


class Registry(object):
    regs = []

    def __call__(self, callback, condition, n=None, millis=None, name=None):
        new_reg = Reg(callback, condition, n, millis, name)

        for idx, reg in enumerate(self.regs):
            if reg.name == new_reg.name:
                self.regs[idx] = new_reg

                break
        else:
            self.regs.append(new_reg)

    def __delitem__(self, item):
        name = item.__name__ if callable(item) else item

        for idx, reg in enumerate(self.regs):
            if reg.name == name:
                del self.regs[idx]

                break
        else:
            raise KeyError("'{}' is not registered".format(item))

    def __iter__(self):
        for reg in self.regs:
            yield reg.name

    def dispatch(self, event, device=None):
        for reg in self.regs:
            if reg.millis is not None:
                if not reg.condition(event):
                    reg.state.millis = 0
                    reg.state.consecutive = 0

                    continue

                reg.state.millis_cur += event.period
                if reg.state.millis_cur > reg.millis:
                    reg.state.millis_cur %= reg.millis

                    reg.callback(event, reg.state.consecutive, reg.name,
                                 device)

                    reg.state.consecutive += 1
            else:
                if not reg.condition(event):
                    reg.state.n = 0

                    continue

                reg.state.n += 1
                if reg.state.n % reg.n == 0:
                    reg.callback(event, int(reg.state.n / reg.n) - 1, reg.name,
                                 device)
