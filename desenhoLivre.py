import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from sys import argv


def init ():
    "Set up several OpenGL state variables"
    # Background color
    glClearColor (1.0, 1.0, 1.0, 1.0)
    # Projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    a = 0
    b = 0
    
    
def display():
    "Does the actual drawing"
    # Clear frame buffer
    glClear (GL_COLOR_BUFFER_BIT);
    # Set draw color to blue
    glColor3f (1.0, 0.0, 0.0)
    # Draw ellipse
    # Flush and swap buffers
    glutSwapBuffers()

def moveMouse(x,y):    
    glBegin(GL_LINE_STRIP)
    glVertex2f(x/600.0,(600.0-y)/600.0)
    glVertex2f(a/600.0,(600.0-b)/600.0)
    glEnd()
    glFlush()
    glutSwapBuffers()
    global a, b
    a = x
    b = y

def mouse( button,  state,  x,  y): 
    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN ):
        global a, b
        a = x
        b = y 
    if(button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN):
        exit(0)

    
glutInit(argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(600,600)
glutCreateWindow("Square")
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutMotionFunc(moveMouse)
init()
glutMainLoop()
