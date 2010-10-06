# -*- coding: utf-8 -*-

from collections import namedtuple
from math import hypot


class Point(namedtuple('Point', 'x y')):
    __slots__ = ()

    @property
    def hypot(self):
        return hypot(self.x, self.y)

    def __add__(self, other):
        return Point.__new__(Point, self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point.__new__(Point, self.x - other.x, self.y - other.y)
    def __lt__(self, other):
        return self.hypot < other.hypot

    def __and__(self, other):
        return tuple.__add__(self, other)


class BaseGraphic(object):
    def __init__(self, top_left, bottom_right):
        # Sort to make sure the coordinates are not inverted
        coordinates = (Point._make(top_left), Point._make(bottom_right))
        self.top_left, self.bottom_right = sorted(coordinates)

    def __contains__(self, (x, y)):
        return (self.top_left.x <= x < self.bottom_right.x) and (self.top_left.y <= y < self.bottom_right.y)

    def __repr__(self):
        return "<%s top_left=%s bottom_right=%s>" % (self.__class__.__name__, self.top_left, self.bottom_right)
