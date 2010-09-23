# -*- coding: utf-8 -*-

# PyRysunek is a simple vector drawing program using OpenGL.
# http://launchpad.net/pyrysunek

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys


class App(object):

    """A simple OpenGL drawing application."""

    LINE_SIZE_THIN = LINE_SIZE_MEDIUM = \
    LINE_SIZE_LARGE = LINE_SIZE_XLARGE = True

    def __init__(self, debug=False, width=800, height=500):
        """Create an instance of a PyRysunek application.

        Keyword arguments:
        debug -- show debug information in the console during program execution
        """
        self.DEBUG = debug
        self.__objects = []
        self.toolbar = Toolbar(0, height-64, width, 64)
        self.line_size = True
        self.width = width
        self.height = height

        self._init_opengl()

    def _init_opengl(self):
        """OpenGL initialization commands."""
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(150, 50)
        glutCreateWindow("PyRysunek")

        # Assign callback functions
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.on_mouse_event)

        # Set background color
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def display(self):
        """Callback to draw the application in the screen."""
        # Clear frame buffer
        glClear(GL_COLOR_BUFFER_BIT)

        self.toolbar.draw()

        # Flush and swap buffers
        glutSwapBuffers()

    def reshape(self, w, h):
        """Callback to adjust the coordinate system whenever a window is
        created, moved or resized.
        """
        self.width, self.height = w, h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Define left, right, bottom, top coordinates
        gluOrtho2D(0.0, w, 0.0, h)

    def on_mouse_event(self, button, state, x, y):
        """Callback to handle mouse events."""
        if self.toolbar.contains(x, y):
            self.toolbar.on_mouse_event(button, state, x, y)
        else:
            if state == GLUT_UP and x and y:
                self.__objects.append(None)
        if self.DEBUG:
            print button, state, x, y
            print "Selected tool:", self.selected_tool
            print "Line size:", self.line_size

    def getObjects(self):
        return self.__objects

    @property
    def selected_tool(self):
        return self.toolbar.selected_tool


class Tool:
    def __repr__(self):
        return "<%s>" % self.__class__.__name__

class SelectionTool(Tool):
    pass

class RectangleTool(Tool):
    pass


class Button:
    def __init__(self, x, y, width, height):
        print x, y, width, height
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def __contains__(self, (x, y)):
        return (self.x <= x < self.width) and (self.y <= y < self.height)

    def draw(self):
        glRectf(self.x, self.y, self.x + self.width, self.y + self.height)
        
class SelectionButton(Button, SelectionTool):
    pass
    
class Toolbar:
    SELECTION_TOOL = SelectionTool()
    RECTANGLE_TOOL = RectangleTool()
    ELLIPSE_TOOL = LINE_TOOL = \
    RESIZE_TOOL = MOVE_TOOL = DELETE_TOOL = True

    def __init__(self, x, y, width, height):
        self.selected_tool = self.SELECTION_TOOL
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__buttons = []
        self.add_button(SelectionButton)

    def contains(self, x, y):
        return (0 <= x < self.width) and (0 <= y < self.height)

    def add_button(self, button_type):
        self.__buttons.append(
            button_type(self.x, self.y, self.height, self.height)
        )
    
    def on_mouse_event(self, button, state, x, y):
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


if __name__ == "__main__":
    # Main Program
    app = App(debug=True)
    glutMainLoop()