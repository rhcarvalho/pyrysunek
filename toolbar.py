# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from buttons import *


class Toolbar(object):
    def __init__(self, config):
        self.config = config

        self.x, self.y = config.position

        self._buttons = []
        self.add_buttons(SelectionButton, RectangleButton, EllipseButton,
            FreeFormButton, ResizeButton, MoveButton, DeleteButton)

        self.current_tool = self._buttons[1]
        
        config.color_picker.update(
            position = (self.width, self.y),
            icon_size = config.icon_size / 2,
            padding = config.padding,
            toolbar_color = config.color,
            toolbar_height = self.height,
        )
        self.color_picker = ColorPicker(config.color_picker)

    def _get_current_tool(self):
        return self.__current_tool
    def _set_current_tool(self, tool):
        for button in self._buttons:
            button.selected = False
        self.__current_tool = tool
        tool.selected = True
    current_tool = property(_get_current_tool, _set_current_tool)

    def __contains__(self, (x, y)):
        x_is_in_boundary = self.x <= x < self.color_picker.x + self.color_picker.width
        y_is_in_boundary = self.y <= y < self.y + self.height
        return x_is_in_boundary and y_is_in_boundary

    def __repr__(self):
        return "%s(config=%s)" % (self.__class__.__name__, self.config)

    @property
    def width(self):
        return len(self._buttons) * (self.config.icon_size + self.config.padding) + self.config.padding

    @property
    def height(self):
        return self.config.icon_size + 2 * self.config.padding

    def add_button(self, button_type):
        size = self.config.icon_size
        padding = self.config.padding
        x = self.x + padding + (size + padding) * len(self._buttons)
        y = self.y + padding
        self._buttons.append(button_type(x, y, size))

    def add_buttons(self, *button_types):
        for button_type in button_types:
            self.add_button(button_type)

    def mouse(self, button, state, x, y):
        if state == GLUT_UP:
            self.select(x, y)

    def draw(self):
        """Draw the toolbar."""
        glColor4fv(self.config.color)
        glRectf(self.x, self.y, self.width, self.height)

        for i in range(len(self._buttons)):
            self._buttons[i].draw()
            
        self.color_picker.draw()

    def select(self, x, y):
        """Find which button was clicked and set current tool"""
        for button in self._buttons:
            if (x, y) in button:
                self.current_tool = button
                break


class ColorPicker(object):
    def __init__(self, config):
        self.config = config

        self.x, self.y = config.position
        self.x += 3 * self.config.padding
        self.height = self.config.toolbar_height

    @property
    def width(self):
        size = self.config.icon_size
        padding = self.config.padding
        return (len(self.config.colors) / 2) * (size + padding) + 3 * (padding + size)
        
    def draw(self):
        """Draw the color picker."""
        glColor4fv(self.config.toolbar_color)
        glRectf(self.x, self.y, self.x + self.width, self.y + self.height)
        
        size = self.config.icon_size
        padding = self.config.padding
        
        x = self.x + padding
        y = self.y + padding
        glColor4fv(self.config.default_fill_color)
        glRectf(x, y, x + size, y + size)
        x = self.x + padding + (size + padding)
        y = self.y + padding + (size + padding / 2.0)
        glColor4fv(self.config.default_line_color)
        glRectf(x, y, x + size, y + size)
        
        colors = (self.config.colors[:len(self.config.colors)/2],
                  self.config.colors[len(self.config.colors)/2:])
        for i, row in enumerate(colors):
            for j, color in enumerate(row):
                glColor4fv(color)
                x = self.x + (3 * padding + 3 * size) + (size + padding) * j
                y = self.y + padding + (size + padding / 2.0) * i
                glRectf(x, y, x + self.config.icon_size, y + self.config.icon_size)
