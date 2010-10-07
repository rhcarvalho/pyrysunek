# -*- coding: utf-8 -*-

# PyRysunek is a simple vector drawing program using OpenGL.
# http://launchpad.net/pyrysunek

# TODO:
# visually identify tools
# move objects
# resize objects
# change colors
# change line size
# refine toolbar appearance

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from config import default
from toolbar import Toolbar


class App(object):

    """A simple OpenGL drawing application."""

    def __init__(self, config=default, debug=False):
        """Create an instance of a PyRysunek application.

        Optional arguments:
        config -- dictionary containing configuration values (see `config.default`)
        debug -- show debug information in the console during program execution
        """
        self.config = config
        self.DEBUG = debug
        
        self.width, self.height = self.config.window_size

        self._objects = []
        self.toolbar = Toolbar(self.config.toolbar)

        self._init_opengl()

    def _init_opengl(self):
        """OpenGL initialization commands."""
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(*self.config.window_position)
        glutCreateWindow(self.config.window_title)

        # Assign callback functions
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)

        # Set background color
        glClearColor(*self.config.bg_color)

    def display(self):
        """Callback to draw the application in the screen."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Clear frame buffer
        glClear(GL_COLOR_BUFFER_BIT)

        for obj in self._objects:
            obj.draw()

        # Make sure that toolbar is on top of everything
        self.toolbar.draw()

        # Flush and swap buffers
        glutSwapBuffers()

    def reshape(self, w, h):
        """Callback to adjust the coordinate system whenever a window is
        created, moved or resized.
        """
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Define left, right, bottom, top coordinates
        gluOrtho2D(0.0, self.width, self.height, 0.0)

    def mouse(self, button, state, x, y):
        """Callback to handle mouse events."""
        if (x, y) in self.toolbar:
            self.toolbar.mouse(button, state, x, y)
        else:
            if state == GLUT_DOWN:
                self.toolbar.current_tool.mouse_down(x, y, self._objects)

            elif state == GLUT_UP:
                self.toolbar.current_tool.mouse_up(x, y, self._objects)

        if self.DEBUG:
            print button, state, x, y
            print "Current tool:", self.toolbar.current_tool
            print "Objects:", self._objects

    def motion(self, x, y):
        self.toolbar.current_tool.mouse_move(x, y, self._objects)

    def keyboard(self, key, x, y):
        # Exit on `ESC` keycode
        if key == "\x1b":
            sys.exit(0)


if __name__ == "__main__":
    # Main Program
    app = App(debug=True)
    glutMainLoop()