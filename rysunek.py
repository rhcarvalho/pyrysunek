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
        self.line_size = True

    def on_mouse_event(self, button, state, x, y):
        """Handle mouse events."""
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
        
class Toolbar:
    SELECTION_TOOL = SelectionTool()
    RECTANGLE_TOOL = RectangleTool()
    ELLIPSE_TOOL = LINE_TOOL = \
    RESIZE_TOOL = MOVE_TOOL = DELETE_TOOL = True

    def __init__(self, width=800, height=64):
        self.selected_tool = self.SELECTION_TOOL
        self.width = width
        self.height = height
        
    def contains(self, x, y):
        return (0 <= x < self.width) and (0 <= y < self.height)
        
    def on_mouse_event(self, button, state, x, y):
        if x >= 64:
            self.selected_tool = True
        else:
            self.selected_tool = self.SELECTION_TOOL
        

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