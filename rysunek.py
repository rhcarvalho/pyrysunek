"""A simple OpenGL program in Python.
Draws a white square on a black background
"""

import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from sys import argv


class App(object):
    LINE_SIZE_THIN = LINE_SIZE_MEDIUM = \
    LINE_SIZE_LARGE = LINE_SIZE_XLARGE = True

    def __init__(self, debug=False):
        self.DEBUG = debug
        self.__objects = []
        self.toolbar = Toolbar()
        self.selected_tool = self.toolbar.selected_tool
        self.line_size = True

    def on_mouse_event(self, button, state, x, y):
        if state == GLUT_UP and x and y:
            self.__objects.append(None)
        if self.DEBUG:
            print button, state, x, y
            print "Selected tool:", self.selected_tool
            print "Line size:", self.line_size

    def getObjects(self):
        return self.__objects


class Toolbar:
    SELECTION_TOOL = RECTANGLE_TOOL = ELLIPSE_TOOL = LINE_TOOL = \
    RESIZE_TOOL = MOVE_TOOL = DELETE_TOOL = True

    selected_tool = True


def init():
    "Set up several OpenGL state variables"
    # Background color
    glClearColor(0.0, 0.0, 0.0, 0.0)
    # Projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)

def display():
    "Does the actual drawing"
    # Clear frame buffer
    glClear(GL_COLOR_BUFFER_BIT);
    # Set draw color to white
    glColor3f(1.0, 1.0, 1.0)
    # Draw square
    glBegin(GL_POLYGON)
    for v in [[0.3,0.3],[0.7, 0.3],[0.7, 0.7],[0.3, 0.7]]:
        glVertex2fv(v)
    glEnd()
    # Flush and swap buffers
    glutSwapBuffers()


if __name__ == "__main__":
    # Main Program
    glutInit(argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(400, 400)
    glutCreateWindow("PyRysunek")
    glutDisplayFunc(display)
    app = App(debug=True)
    glutMouseFunc(app.on_mouse_event)
    init()
    glutMainLoop()