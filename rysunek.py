# -*- coding: utf-8 -*-

# PyRysunek is a simple vector drawing program using OpenGL.
# http://launchpad.net/pyrysunek

# TODO:
# draw rectangles
# draw ellipses
# select tools
# draw lines
# move objects
# resize objects
# change colors
# change line size

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


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
                self.__objects.append(Rectangle(x, y, x, y))
                
            elif state == GLUT_UP:
                self.__objects[-1].done = True
        
        if self.DEBUG:
            print button, state, x, y
            print "Selected tool:", self.selected_tool
            print "Line size:", self.line_size
            print "Objects:", self.__objects
    
    def motion(self, x, y):
        # update last object
        obj = self.__objects[-1]
        obj.width = x
        obj.height = y

    def keyboard(self, key, x, y):
        if key == "\x1b":
            sys.exit(0)

    @property
    def selected_tool(self):
        return self.toolbar.selected_tool


class Tool(object):
    def __repr__(self):
        return "<%s>" % self.__class__.__name__

class SelectionTool(Tool):
    pass

class RectangleTool(Tool):
    pass

class EllipseTool(Tool):
    pass

class LineTool(Tool):
    pass

class ResizeTool(Tool):
    pass

class MoveTool(Tool):
    pass

class DeleteTool(Tool):
    pass


class BaseGraphic(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __contains__(self, (x, y)):
        return (self.x <= x < self.width) and (self.y <= y < self.height)
        
    def __repr__(self):
        return "<%s x=%s y=%s w=%s h=%s>" % (self.__class__.__name__, self.x, self.y, self.width, self.height)


class Button(BaseGraphic):
    def draw(self):
        glRectf(self.x, self.y, self.x + self.width, self.y + self.height)


class SelectionButton(Button, SelectionTool):
    pass


class RectangleButton(Button, RectangleTool):
    pass


class EllipseButton(Button, EllipseTool):
    pass


class LineButton(Button, LineTool):
    pass


class ResizeButton(Button, ResizeTool):
    pass


class MoveButton(Button, MoveTool):
    pass


class DeleteButton(Button, DeleteTool):
    pass


class Toolbar(BaseGraphic):
    def __init__(self, x, y, width, height):
        super(Toolbar, self).__init__(x, y, width, height)
        self.__buttons = []
        self.add_buttons(SelectionButton, RectangleButton, EllipseButton,
            LineButton, ResizeButton, MoveButton, DeleteButton)
        self.selected_tool = self.__buttons[0]

    def add_button(self, button_type):
        size = self.height
        x = self.x + size * len(self.__buttons)
        y = self.y
        self.__buttons.append(button_type(x, y, size, size))

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


class Rectangle(BaseGraphic):
    def __init__(self, *args):
        super(Rectangle, self).__init__(*args)
        #self.color = glGetFloatv(GL_CURRENT_COLOR)
        self.color = (0.08, 0.08, 0.54, 1.0) # Force color
        self.done = False
        
    def draw(self):
        if not self.done:
            # draw guides in the first and last corners
            quadratic = gluNewQuadric()
            r, g, b, a = self.color
            inverse_color = (1-r, 1-g, 1-b, a)
            glColor4fv(inverse_color)
            glPushMatrix()
            glTranslatef(self.x, self.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(self.width, self.height, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
        glColor4fv(self.color)
        glRectf(self.x, self.y, self.width, self.height)


if __name__ == "__main__":
    # Main Program
    app = App(debug=True)
    glutMainLoop()