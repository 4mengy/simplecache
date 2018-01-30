#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['cache_factory']

import pickle
import time
from abc import ABCMeta, abstractmethod

from randomdict import RandomDict


class CacheStorage(object):
    __meta__ = ABCMeta

    @abstractmethod
    def put(self, key, val):
        """Put key value into _cache"""

    @abstractmethod
    def get(self, key, default=None):
        """Return value of key. If not in _cache, return default"""

    @abstractmethod
    def clear(self):
        """Remove all entries"""

    @abstractmethod
    def invalidate(self, key):
        """Remove key from _cache"""

    def load(self, *args, **kwargs):
        """Load _cache from external"""

    def dump(self, *args, **kwargs):
        """Dump _cache to external"""


class RandomCacheStorage(CacheStorage):
    def __init__(self, size, time_out):
        self.size = size
        self.time_out = time_out
        self.slot = RandomDict()
        self.clock = {}
        self.ver = '0.1'

    def put(self, key, val):
        if len(self.slot) == self.size:
            k = self.slot.randdel()
            del self.clock[k]
        self.slot[key] = val
        self.clock[key] = time.time()

    def get(self, key, default=None):
        if key not in self.clock:
            return default

        if time.time() - self.clock[key] > self.time_out:
            self.invalidate(key)
            return default

        return self.slot[key]

    def clear(self):
        self.slot.clear()
        self.clock.clear()

    def invalidate(self, key):
        del self.slot[key]
        del self.clock[key]

    def load(self, fp):
        slot, clock, ver = pickle.load(fp)
        if self.ver == ver:
            self.slot = slot
            self.clock = clock

    def dump(self, fp):
        pickle.dump((self.slot, self.clock, self.ver), fp)


_IGNORE_MARKER = object()
_MARKER = object()


def cache_factory(maxsize, time_out, ignore_return=(_IGNORE_MARKER,), ignore_unhashable_args=False):
    class Cache(object):
        def __init__(self):
            self._cache = RandomCacheStorage(maxsize, time_out)
            self._ignore_return = ignore_return
            self._ignore_unhashable_args = ignore_unhashable_args

        def __call__(self, func):
            _cache = self._cache
            marker = _MARKER

            def cached_wrapper(*args, **kwargs):
                try:
                    key = (args, frozenset(kwargs.items())) if kwargs else args
                    hash(key)
                except TypeError as e:
                    if self._ignore_unhashable_args:
                        return func(*args, **kwargs)
                    else:
                        raise e

                val = _cache.get(key, marker)
                if val is marker:
                    val = func(*args, **kwargs)
                    if val not in self._ignore_return:
                        _cache.put(key, val)
                return val

            return cached_wrapper

        def load(self, fp):
            self._cache.load(fp)

        def dump(self, fp):
            self._cache.dump(fp)

    return Cache()
