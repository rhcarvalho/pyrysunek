# -*- coding: utf-8 -*-

# PyRysunek is a simple vector drawing program using OpenGL.
# http://launchpad.net/pyrysunek

# TODO:
# change line size
# -- bonus --
# better selection overlay
# transparent color (draw without fill or outline)
# Buttons to Save / Load actions
# SelectionTool behavior according to the Red Book
# group/ungroup objects
# rotate tool
# bring to front / send to back

# ** turn off DEBUG and AUTORELOAD **

import cPickle as pickle
import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from config import default, DEBUG
from toolbar import Toolbar


class App(object):

    """A simple OpenGL drawing application."""

    def __init__(self, config=default):
        """Create an instance of a PyRysunek application.

        Optional arguments:
        config -- dictionary containing configuration values (see `config.default`)
        """
        self.config = config
        self.width, self.height = self.config.window_size

        self.toolbar = Toolbar(self.config.toolbar)
        self.context = Context(
            objects = ObjectList(),
            color_picker = self.toolbar.color_picker,
        )

        self._init_opengl()

        if config.auto_load_on_start:
            self.load()

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

        for obj in self.context.objects:
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
                self.toolbar.current_tool.mouse_down(x, y, self.context)

            elif state == GLUT_UP:
                self.toolbar.current_tool.mouse_up(x, y, self.context)

        if DEBUG:
            print "<Mouse click event>"
            print "  button=%s, state=%s, x=%s, y=%s" % (button, state, x, y)
            print "  current_tool = %s" % self.toolbar.current_tool
            print "  len(objects) = %s" % len(self.context.objects)
            print "  objects[-3:] = %s" % self.context.objects[-3:]

    def motion(self, x, y):
        self.toolbar.current_tool.mouse_move(x, y, self.context)

    def keyboard(self, key, x, y):
        if key == "\x1b":
            # Exit on `ESC` keycode.
            sys.exit(0)
        elif key == "\x13":
            # Ctrl+s
            self.save()
        elif key == "\x12":
            # Ctrl+r
            self.load()
        else:
            # Propagate event to toolbar.
            self.toolbar.keyboard(key, x, y)

    def save(self):
        """Save the current objects to disk.

        Fail silently if `self.config.temp_file` fails to open.

        """
        try:
            temp_file = open(self.config.temp_file, "wb")
            pickle.dump(self.context.objects, temp_file)
            temp_file.close()
            if DEBUG:
                print "<Saved objects>"
        except IOError:
            if DEBUG:
                print "<Failed to save objects>"

    def load(self):
        """Load objects from disk.

        Fail silently if `self.config.temp_file` fails to open.

        """
        try:
            temp_file = open(self.config.temp_file, "rb")
            self.context.objects = pickle.load(temp_file)
            temp_file.close()
            if DEBUG:
                print "<Load objects>"
        except IOError:
            if DEBUG:
                print "<Failed to load objects>"


class Context(dict):
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        return self.__setitem__(name, value)

    def __delattr__(self, name):
        return self.__delitem__(name)


class ObjectList(list):
    def __init__(self, iterable=()):
        super(ObjectList, self).__init__(iterable)
        self.selected = None

    def select_none(self):
        for obj in self:
            obj.selected = False
        self.selected = None

    def select(self, x, y):
        self.select_none()
        for obj in reversed(self):
            if (x, y) in obj:
                obj.selected = True
                self.selected = obj
                break


def main():
    """Run main program loop."""
    app = App()
    glutMainLoop()


if __name__ == "__main__":
    if DEBUG:
        import autoreload
        autoreload.main(main)
    else:
        main()
