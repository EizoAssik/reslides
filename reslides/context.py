# encoding=utf-8

from collections import deque

class Context:
    pass


class FileContext(Context):
    def __init__(self, path, mode='r'):
        try:
            self._file = open(path, mode)
        except FileNotFoundError as e:
            raise e
        self._iter = None
        self._curr = None
        self._prec = deque(maxlen=64)
        self._succ = deque()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            try:
                self._file.close()
            except:
                pass

    def __iter__(self):
        if self._iter is None:
            self._iter = FileContextIter(self)
        return self._iter

    def __next__(self):
        if self._iter is None:
            self._iter = FileContextIter(self)
        return next(self._iter)

    def back(self):
        if self._prec:
            self._succ.appendleft(self._curr)
            self._curr = self._prec.pop()

    def glance(self):
        if not self._succ:
            line = self._file.readline()
            self._succ.append(line)
        self._prec.append(self._curr)
        self._curr = self._succ.popleft()
        return self._curr

    def insert(self, line, after=False):
        if after:
            self._succ.appendleft(line)
        else:
            self._succ.appendleft(self._curr)
            self._curr = line


class FileContextIter:
    def __init__(self, fc: FileContext):
        self.fc = fc

    def __iter__(self):
        return self

    def __next__(self):
        if self.fc._curr is None:
            self.fc.glance()
        line = self.fc._curr
        if not line:
            raise StopIteration()
        self.fc.glance()
        return line


class ApplyContext(Context):
    def __init__(self, fc, rules):
        self._fc = fc
        self._iter = None
        self._rules = rules

    def __iter__(self):
        if self._iter is None:
            self._iter = ApplyContextIter(self)
        return self._iter

    def __next__(self):
        if self._iter is None:
            self._iter = ApplyContextIter(self)
        return next(self._iter)

class ApplyContextIter:
    def __init__(self, ac):
        self.ac = ac
        self.cleanup = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            for rule in self.ac._rules:
                rule.apply(self.ac._fc)
            return next(self.ac._fc)
        except StopIteration:
            if self.cleanup is None:
                self.cleanup = iter(self.ac._fc._succ)
            return next(self.cleanup)




