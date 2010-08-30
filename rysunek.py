"""A simple OpenGL program in Python.
Draws a white square on a black background
"""

import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from sys import argv


class App(object):
    def __init__(self):
        self.__objects = []

    def getToolbar(self):
        return Toolbar()
        
    def onMouseEvent(self, button, state, x, y):
        if state == GLUT_UP and x and y:
            self.__objects.append(None)
        
    def getObjects(self):
        return self.__objects

class Toolbar:
    def getButton(self, index):
        return Button()
        
class Button:
    def click(self):
        return True
        

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
    app = App()
    glutMouseFunc(app.onMouseEvent)
    init()
    glutMainLoop()