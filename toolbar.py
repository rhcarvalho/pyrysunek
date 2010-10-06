# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from buttons import *


class Toolbar(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
        self._buttons = []
        self.add_buttons(SelectionButton, RectangleButton, EllipseButton,
            LineButton, ResizeButton, MoveButton, DeleteButton)

    def __contains__(self, (x, y)):
        return (self.x <= x < self.x + self.width) and (self.y <= y < self.y + self.height)

    def __repr__(self):
        return "%s(x=%s y=%s width=%s height=%s)" % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def add_button(self, button_type):
        size = self.height
        x = self.x + size * len(self._buttons)
        y = self.y
        self._buttons.append(button_type((x, y), (x + size, y + size)))

    def add_buttons(self, *button_types):
        for button_type in button_types:
            self.add_button(button_type)

    def mouse(self, button, state, x, y):
        pass

    def draw(self):
        """Draw the toolbar."""
        colors = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.5, 0.7, 0.6),
        )
        for i in range(len(self._buttons)):
            glColor3fv(colors[i % len(colors)])
            self._buttons[i].draw()
