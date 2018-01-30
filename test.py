#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import unittest

from randomdict import RandomDict
from cache import RandomCacheStorage


class TestRandomDict(unittest.TestCase):
    def test_set_get(self):
        t = RandomDict()
        t['a'] = 1
        t['b'] = 2
        self.assertEqual(1, t['a'])
        self.assertEqual(2, t['b'])

        t['a'] = 10
        self.assertEqual(10, t['a'])
        self.assertEqual(2, t['b'])
        self.assertEqual(2, len(t))
        self.assertEqual(2, t.get('b'))

        t.setdefault('c', 89)
        self.assertEqual(89, t['c'])

    def test_del(self):
        t = RandomDict()
        t['a'] = 1
        t['b'] = 2

        del t['a']

        self.assertEqual(2, t['b'])
        self.assertEqual(1, len(t))
        self.assertEqual(2, t.pop('b'))
        self.assertEqual(0, len(t))

    def test_update(self):
        t = RandomDict({'a': 1, 'b': 2})
        self.assertEqual(2, len(t))
        self.assertEqual(1, t['a'])
        self.assertEqual(2, t['b'])

        t.update({'c': 7, 'a': 8})
        self.assertEqual(3, len(t))
        self.assertEqual(8, t['a'])
        self.assertEqual(2, t['b'])
        self.assertEqual(7, t['c'])


class TestRandomCacheStorage(unittest.TestCase):
    def test_set_get(self):
        t = RandomCacheStorage(2, 10)
        t.put(1, 1)
        t.put(1, 3)
        self.assertEqual(3, t.get(1))
        self.assertEqual(1, len(t.clock))
        self.assertEqual(1, len(t.slot))

    def test_timeout(self):
        t = RandomCacheStorage(2, 10)
        t.put(1, 1)
        time.sleep(11)

        self.assertEqual(None, t.get(1))
        self.assertEqual(0, len(t.clock))
        self.assertEqual(0, len(t.slot))

    def test_invalidate(self):
        t = RandomCacheStorage(2, 10)
        t.put(1, 1)
        t.put(3, 1)
        t.invalidate(1)
        self.assertEqual(None, t.get(1))
        self.assertEqual(1, t.get(3))
        self.assertEqual(1, len(t.clock))
        self.assertEqual(1, len(t.slot))

    def test_clear(self):
        t = RandomCacheStorage(2, 10)
        t.put(1, 1)
        t.put(3, 1)
        t.clear()
        self.assertEqual(0, len(t.clock))
        self.assertEqual(0, len(t.slot))


if __name__ == '__main__':
    unittest.main()
