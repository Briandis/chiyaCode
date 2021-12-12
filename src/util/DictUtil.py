import inspect
import re


class Dict(dict):

    def __getitem__(self, key):
        s = inspect.stack()
        k = re.findall("\[.*?\.(.*?)\]", s[1][-2][0])

        if len(k) == 0:
            return self.get(key)
        l = k[0].split(".")
        if len(l) == 1:
            return self.get(key)
        d = self
        for i in l:
            if d is None or type(d) is not Dict:
                return None
            d = d.get(i)
        return d

    def __setitem__(self, key, value):
        s = inspect.stack()
        k = re.findall("\[.*?\.(.*?)\]", s[-1][-2][0])
        if len(k) == 0:
            super().__setitem__(key, value)
            return
        d = self
        size = k[0].split(".")
        for i in range(len(size)):
            if i == len(size) - 1:
                d.set(size[i], value)
            if size[i] not in d:
                d.set(size[i], Dict())
            d = d.get(size[i])

    def set(self, key, value):
        super().__setitem__(key, value)
