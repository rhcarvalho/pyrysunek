from math import *
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Elipse:

    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.x = x #coordenada x do centro
        self.y = y #coordenada y do centro

    def drawElipse(self):
        for i in range(360):
            angle = 2*pi*i/360
            glVertex2f (self.a*cos(angle)+self.x, self.b*sin(angle)+self.y)
        glEnd()
    
