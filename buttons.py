# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import BaseGraphic
from tools import *


class Button(BaseGraphic):
    def draw(self):
        glRectf(self.top_left.x, self.top_left.y, self.top_left.x + self.bottom_right.x, self.top_left.y + self.bottom_right.y)


class SelectionButton(Button, SelectionTool):
    pass


class RectangleButton(Button, RectangleTool):
    pass


class EllipseButton(Button, EllipseTool):
    pass


class LineButton(Button, LineTool):
    pass


class ResizeButton(Button, ResizeTool):
    pass


class MoveButton(Button, MoveTool):
    pass


class DeleteButton(Button, DeleteTool):
    pass