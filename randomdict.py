#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
from collections import MutableMapping


class RandomDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__slot = []
        self.__keys = {}

        if args or kwargs:
            self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if key not in self.__keys:
            i = len(self)
            self.__keys[key] = i
            self.__slot.append([key, value])
        else:
            index = self.__keys[key]
            self.__slot[index][1] = value

    def __getitem__(self, item):
        index = self.__keys[item]
        return self.__slot[index][1]

    def __delitem__(self, key):
        index = self.__keys[key]
        last_key, last_val = self.__slot[-1]
        if index != len(self) - 1:
            self.__keys[last_key] = index
            self.__slot[index] = [last_key, last_val]
        del self.__keys[key]
        del self.__slot[-1]

    def __len__(self):
        return len(self.__keys)

    def __iter__(self):
        return iter(self.__keys)

    def randkey(self):
        if len(self) == 0:
            raise KeyError

        i = random.randint(0, len(self) - 1)
        return self.__slot[i][0]

    def randvalue(self):
        k = self.randkey()
        return self[k]

    def randitem(self):
        k = self.randkey()
        return k, self[k]

    def randdel(self):
        k = self.randkey()
        del self[k]
        return k
