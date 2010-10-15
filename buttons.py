# -*- coding: utf-8 -*-

try:
    import Image
except ImportError:
    print "A required library is not available: Python Imaging Library (PIL)"
    raise
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from tools import *


class Button(object):

    """Represent a graphic button."""

    def  __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.selected = False

    def __contains__(self, (x, y)):
        return ((self.x <= x < self.x + self.size) and
                (self.y <= y < self.y + self.size))

    def __repr__(self):
        return "%s(x=%s, y=%s, size=%s)" % (self.__class__.__name__, self.x, self.y, self.size)

    def draw(self):
        """Draw itself using OpenGL primitives."""
        glColor4fv(self.color)
        glRectf(self.x, self.y, self.x + self.size, self.y + self.size)


class IconicButton(Button):

    """Represent a button with a nice icon.

    Requires PIL.

    """

    icon_name = None # Must be defined on subclass

    def  __init__(self, x, y, size, color):
        super(IconicButton, self).__init__(x, y, size, color)

        # Load an image file as a 2D texture using PIL
        icon_path = "icons/%dx%d/%s.png" % (self.size, self.size, self.icon_name)
        try:
            im = Image.open(icon_path)
            self.icon_width = im.size[0]
            self.icon_height = im.size[1]
            self.icon_image = im.tostring("raw", "RGBA", 0, -1)
        except IOError:
            print "PyRysunek was unable to load an icon from %s" % icon_path
            raise

    def draw(self):
        """Draw itself using OpenGL primitives."""
        glEnable(GL_TEXTURE_2D)
        gluBuild2DMipmaps(
            GL_TEXTURE_2D, 3, self.icon_width, self.icon_height,
            GL_RGBA, GL_UNSIGNED_BYTE, self.icon_image
        )

        if self.selected:
            color = self.color
        else:
            color = (1.0, 1.0, 1.0, 1.0)
        glColor4fv(color)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(self.x, self.y + self.size)
        glTexCoord2f(1, 0)
        glVertex2f(self.x + self.size, self.y + self.size)
        glTexCoord2f(1, 1)
        glVertex2f(self.x + self.size, self.y)
        glTexCoord2f(0, 1)
        glVertex2f(self.x, self.y)
        glEnd()
        glDisable(GL_TEXTURE_2D)


class SelectionButton(IconicButton, SelectionTool):
    icon_name = "tool-pointer"


class RectangleButton(IconicButton, RectangleTool):
    icon_name = "draw-rectangle"


class EllipseButton(IconicButton, EllipseTool):
    icon_name = "draw-ellipse"


class FreeFormButton(IconicButton, FreeFormTool):
    icon_name = "draw-freehand"


class ResizeButton(IconicButton, ResizeTool):
    icon_name = "transform-scale-horizontal"


class MoveButton(IconicButton, MoveTool):
    icon_name = "transform-move-horizontal"


class DeleteButton(IconicButton, DeleteTool):
    icon_name = "draw-eraser-delete-objects"


class SetColorButton(Button):
    pass
