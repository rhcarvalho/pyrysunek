# -*- coding: utf-8 -*-

import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import Point
from tools import *


class Button(object):
    icon_name = None # Must be defined on subclass

    def  __init__(self, offset, size):
        self.offset = Point._make(offset)
        self.size = size

        self.selected = False

        # Load an image file as a 2D texture using PIL
        icon_path = "icons/%dx%d/%s.png" % (self.size, self.size, self.icon_name)
        im = Image.open(icon_path)
        self.icon_width = im.size[0]
        self.icon_height = im.size[1]
        self.icon_image = im.tostring("raw", "RGBA", 0, -1)

    def __contains__(self, (x, y)):
        return ((self.offset.x <= x < self.offset.x + self.size) and
                (self.offset.y <= y < self.offset.y + self.size))

    def __repr__(self):
        return "%s(offset=%s, size=%s)" % (self.__class__.__name__, self.offset, self.size)

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        gluBuild2DMipmaps(
            GL_TEXTURE_2D, 3, self.icon_width, self.icon_height,
            GL_RGBA, GL_UNSIGNED_BYTE, self.icon_image
        )

        if self.selected:
            glColor3f(0.82, 0.82, 0.95)
        else:
            glColor3f(1, 1, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.offset.x, self.offset.y + self.size)
        glTexCoord2f(1, 0)
        glVertex2f(self.offset.x + self.size, self.offset.y + self.size)
        glTexCoord2f(1, 1)
        glVertex2f(self.offset.x + self.size, self.offset.y)
        glTexCoord2f(0, 1)
        glVertex2f(self.offset.x, self.offset.y)
        glEnd()


class SelectionButton(Button, SelectionTool):
    icon_name = "tool-pointer"


class RectangleButton(Button, RectangleTool):
    icon_name = "draw-rectangle"


class EllipseButton(Button, EllipseTool):
    icon_name = "draw-ellipse"


class FreeFormButton(Button, FreeFormTool):
    icon_name = "draw-freehand"


class ResizeButton(Button, ResizeTool):
    icon_name = "transform-scale-horizontal"


class MoveButton(Button, MoveTool):
    icon_name = "transform-move-horizontal"


class DeleteButton(Button, DeleteTool):
    icon_name = "draw-eraser-delete-objects"
