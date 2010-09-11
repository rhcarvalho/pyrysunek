import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from sys import argv
from math import *
from elipse import *

def init ():
    "Set up several OpenGL state variables"
    # Background color
    glClearColor (1.0, 1.0, 1.0, 1.0)
    # Projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)


def display():
    "Does the actual drawing"
    # Clear frame buffer
    glClear (GL_COLOR_BUFFER_BIT);
    # Set draw color to blue
    glColor3f (1.0, 0.0, 0.0)
    # Draw ellipse
    glBegin(GL_LINE_LOOP)
    elipse = Elipse(0.5, 0.3, 0.5, 0.5)
    elipse.drawElipse()   
    # Flush and swap buffers
    glutSwapBuffers()


glutInit(argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(600,600)
glutCreateWindow("Elipse")
glutDisplayFunc(display)
init()
glutMainLoop()
