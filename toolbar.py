# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from buttons import *
from geometry import BaseGraphic


class Toolbar(BaseGraphic):
    def __init__(self, top_left, bottom_right):
        super(Toolbar, self).__init__(top_left, bottom_right)
        
        self.x, self.y = top_left
        self.width, self.height = bottom_right
        
        self.__buttons = []
        self.add_buttons(SelectionButton, RectangleButton, EllipseButton,
            LineButton, ResizeButton, MoveButton, DeleteButton)
        self.selected_tool = self.__buttons[0]

    def add_button(self, button_type):
        size = self.height
        x = self.x + size * len(self.__buttons)
        y = self.y
        self.__buttons.append(button_type((x, y), (size, size)))

    def add_buttons(self, *button_types):
        for button_type in button_types:
            self.add_button(button_type)

    def mouse(self, button, state, x, y):
        if x >= 64:
            self.selected_tool = True
        else:
            self.selected_tool = self.SELECTION_TOOL

    def draw(self):
        """Draw the toolbar."""
        colors = (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 1.0, 0.0),
            (0.5, 0.7, 0.6),
        )
        for i in range(len(self.__buttons)):
            glColor3fv(colors[i % len(colors)])
            self.__buttons[i].draw()
