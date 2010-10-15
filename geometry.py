# -*- coding: utf-8 -*-

from collections import namedtuple
from math import hypot


class Point(namedtuple('Point', 'x y')):

    """A useful and pragmatic implementation of a Point.

    May also be used as a vector under some circunstances.
    Refer to the unit tests for examples of usage.

    """

    __slots__ = ()

    @property
    def hypot(self):
        return hypot(self.x, self.y)

    def __add__(self, other):
        return Point.__new__(Point, self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point.__new__(Point, self.x - other.x, self.y - other.y)
    def __mul__(self, number):
        return Point.__new__(Point, self.x * number, self.y * number)
    def __div__(self, number):
        return Point.__new__(Point, self.x / number, self.y / number)
    def __lt__(self, other):
        return self.hypot < other.hypot

    def __and__(self, other):
        return tuple.__add__(self, other)
