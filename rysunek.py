"""A simple OpenGL program in Python.
Draws a white square on a black background
"""

import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from sys import argv

def init ():
    "Set up several OpenGL state variables"
    # Background color
    glClearColor (0.0, 0.0, 0.0, 0.0)
    # Projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)

def display():
    "Does the actual drawing"
    # Clear frame buffer
    glClear (GL_COLOR_BUFFER_BIT);
    # Set draw color to white
    glColor3f (1.0, 1.0, 1.0)
    # Draw square
    glBegin(GL_POLYGON)
    for v in [[0.3,0.3],[0.7, 0.3],[0.7, 0.7],[0.3, 0.7]]:
        glVertex2fv (v)
    glEnd()
    # Flush and swap buffers
    glutSwapBuffers()

# Main Program
glutInit(argv) 
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(400, 400)
glutCreateWindow("Square")
glutDisplayFunc(display)
init()
glutMainLoop()