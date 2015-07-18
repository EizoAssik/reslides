# encoding=utf-8

def argcount(fn):
    return fn.__code__.co_argcount

class Rule:
    def __init__(self, fn, passerby=None):
        self.args = argcount(fn)
        self.fn = fn
        self.passerby = passerby

    def modify(self, result, fc):
        pass

    def apply(self, fc):
        try:
            lines = [None] * self.args
            count = 0
            while count < self.args:
                lines[count] = next(fc)
                count += 1
        except StopIteration:
            for _ in range(count):
                fc.back()
            return
        result = self.fn(*lines)
        self.modify(result, fc)

__rules__ = []

class Remove(Rule):
    def modify(self, result, fc):
        if not (isinstance(result, bool) and result is True):
            for _ in range(self.args):
                fc.back()

class Replace(Rule):
    def modify(self, result, fc):
        if isinstance(result, list):
            for line in result:
                fc.insert(line)
        elif isinstance(result, str):
            fc.insert(result)

def rule(r):
    if isinstance(r, Rule):
        __rules__.append(r)

def passerby(*args):
    def _passerby(fn_or_r):
        if isinstance(fn_or_r, Rule):
            fn_or_r.passerby = args
            return fn_or_r
        return fn_or_r
    return _passerby

def remove(fn):
    if isinstance(fn, Rule):
        return fn
    return Remove(fn, None)

def replace(fn):
    if isinstance(fn, Rule):
        return fn
    return Replace(fn, None)

def getrules():
    return __rules__