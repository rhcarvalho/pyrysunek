# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import BaseGraphic
from tools import *


class Button(BaseGraphic):
    def draw(self):
        glRectf(*(self.top_left & self.bottom_right))


class SelectionButton(Button, SelectionTool):
    pass


class RectangleButton(Button, RectangleTool):
    pass


class EllipseButton(Button, EllipseTool):
    pass


class FreeFormButton(Button, FreeFormTool):
    pass


class ResizeButton(Button, ResizeTool):
    pass


class MoveButton(Button, MoveTool):
    pass


class DeleteButton(Button, DeleteTool):
    pass