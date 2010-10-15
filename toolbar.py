# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from buttons import *


class Toolbar(object):

    """A toolbar with buttons and color picker."""

    def __init__(self, config):
        """Create an instance of Toolbar using a given configuration."""
        self.config = config

        self.x, self.y = config.position

        self._buttons = []
        self._keyboard_shortcuts = {}
        self.add_buttons(
            ('s', SelectionButton),
            ('r', RectangleButton),
            ('e', EllipseButton),
            ('f', FreeFormButton),
            ('x', ResizeButton),
            ('m', MoveButton),
            ('d', DeleteButton),
        )

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

    def add_button(self, key, button_type):
        """Append a button to the end of the toolbar.

        key -- a keyboard shortcut key for easy access.
        button_type -- a button-like class from which a new button will be created.

        """
        size = self.config.icon_size
        padding = self.config.padding

        x = self.x + padding + (size + padding) * len(self._buttons)
        y = self.y + padding
        button = button_type(x, y, size, self.config.selection_color)

        self._buttons.append(button)
        self._keyboard_shortcuts.update({key: button})

    def add_buttons(self, *args):
        """Mass add buttons.

        Expect as argument a number of (key, button_type) pairs to be passed to
        the `add_button` method.

        """
        for key, button_type in args:
            self.add_button(key, button_type)

    def mouse(self, button, state, x, y):
        """Handle mouse clicks on the toolbar area."""
        if state == GLUT_UP:
            if (x, y) in self.color_picker:
                if button == GLUT_LEFT_BUTTON:
                    self.color_picker.set_fill_color(x, y)
                if button == GLUT_RIGHT_BUTTON:
                    self.color_picker.set_line_color(x, y)
            else:
                self.select(x, y)

    def keyboard(self, key, x, y):
        """Handle key down events."""
        if key in self._keyboard_shortcuts:
            self.current_tool = self._keyboard_shortcuts[key]

    def draw(self):
        """Draw the toolbar."""
        # Draw background.
        glColor4fv(self.config.color)
        glRectf(self.x, self.y, self.x + self.width, self.y + self.height)

        for button in self._buttons:
            button.draw()

        self.color_picker.draw()

    def select(self, x, y):
        """Find which button was clicked and set current tool"""
        for button in self._buttons:
            if (x, y) in button:
                self.current_tool = button
                break


class ColorPicker(object):

    """A customizable Color Picker."""

    def __init__(self, config):
        """Create a new instance using the given configuration."""
        self.config = config

        self.x, self.y = config.position
        self.x += 3 * config.padding
        self.height = config.toolbar_height

        self._buttons = []
        self.add_buttons(0, config.colors[:len(config.colors)/2])
        self.add_buttons(1, config.colors[len(config.colors)/2:])

        self.current_fill_color = config.default_fill_color
        self.current_line_color = config.default_line_color

    def __contains__(self, (x, y)):
        x_is_in_boundary = self.x <= x < self.x + self.width
        y_is_in_boundary = self.y <= y < self.y + self.height
        return x_is_in_boundary and y_is_in_boundary

    @property
    def width(self):
        size = self.config.icon_size
        padding = self.config.padding
        return (len(self.config.colors) / 2) * (size + padding) + 3 * (padding + size)

    def add_button(self, line, pos, color):
        """Append a (color) button to the color picker.

        line -- zero based index of the line of the color picker where this button will be.
                Usually 0 or 1.
        pos -- zero based index of the button within its line.
        color -- color activated when the button is clicked.

        """
        size = self.config.icon_size
        padding = self.config.padding
        x = self.x + (3 * padding + 3 * size) + (size + padding) * pos
        y = self.y + padding + (size + padding / 2.0) * line
        self._buttons.append(SetColorButton(x, y, size, color))

    def add_buttons(self, line, colors):
        """Mass add buttons.

        Expect as argument the line which will have new buttons, and a sequence
        of color values specified as a 4-item tuple.

        """
        for pos, color in enumerate(colors):
            self.add_button(line, pos, color)

    def draw(self):
        """Draw the color picker."""
        # Draw background.
        glColor4fv(self.config.toolbar_color)
        glRectf(self.x, self.y, self.x + self.width, self.y + self.height)

        size = self.config.icon_size
        padding = self.config.padding

        # Draw current_fill_color.
        x = self.x + padding
        y = self.y + padding
        glColor4fv(self.current_fill_color)
        glRectf(x, y, x + size, y + size)

        # Draw current_line_color.
        x = self.x + padding + (size + padding)
        y = self.y + padding + (size + padding / 2.0)
        glColor4fv(self.current_line_color)
        glRectf(x, y, x + size, y + size)

        for button in self._buttons:
            button.draw()

    def set_fill_color(self, x, y):
        """Set the current fill color to the one of the button at x, y."""
        for button in self._buttons:
            if (x, y) in button:
                self.current_fill_color = button.color
                break

    def set_line_color(self, x, y):
        """Set the current line color to the one of the button at x, y."""
        for button in self._buttons:
            if (x, y) in button:
                self.current_line_color = button.color
                break
