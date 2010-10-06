# -*- coding: utf-8 -*-

# PyRysunek is a simple vector drawing program using OpenGL.
# http://launchpad.net/pyrysunek

# TODO:
# draw ellipses
# select tools
# draw lines
# move objects
# resize objects
# change colors
# change line size
# refine toolbar appearance

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from drawables import *
from toolbar import Toolbar


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
        self.toolbar = Toolbar(0, 0, width, 64)
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
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        # Set background color
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def display(self):
        """Callback to draw the application in the screen."""
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Clear frame buffer
        glClear(GL_COLOR_BUFFER_BIT)
        
        for obj in self.__objects:
            obj.draw()

        # Make sure that toolbar is on top of everything
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
        gluOrtho2D(0.0, w, h, 0.0)

    def mouse(self, button, state, x, y):
        """Callback to handle mouse events."""
        if (x, y) in self.toolbar:
            self.toolbar.mouse(button, state, x, y)
        else:
            if state == GLUT_DOWN:
                self.__objects.append(Ellipse((x, y), (x, y)))
                
            elif state == GLUT_UP and self.__objects:
                self.__objects[-1].done = True
        
        if self.DEBUG:
            print button, state, x, y
            print "Objects:", self.__objects
    
    def motion(self, x, y):
        # update last object
        if self.__objects:
            obj = self.__objects[-1]
            obj.motion(x, y)

    def keyboard(self, key, x, y):
        if key == "\x1b":
            sys.exit(0)


if __name__ == "__main__":
    # Main Program
    app = App(debug=True)
    glutMainLoop()