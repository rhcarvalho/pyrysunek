# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import BaseGraphic, Point


class Rectangle(BaseGraphic):
    def __init__(self, top_left, bottom_right):
        super(Rectangle, self).__init__(top_left, bottom_right)
        #self.color = glGetFloatv(GL_CURRENT_COLOR)
        self.color = (0.08, 0.08, 0.54, 1.0) # Force color
        self.done = False
        self.selected = False
        self._translate = Point(0, 0)

    def draw(self):
        if not self.done:
            # draw guides in the first and last corners
            quadratic = gluNewQuadric()
            r, g, b, a = self.color
            inverse_color = (1-r, 1-g, 1-b, a)
            glColor4fv(inverse_color)
            glPushMatrix()
            glTranslatef(self.top_left.x, self.top_left.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(self.bottom_right.x, self.bottom_right.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
        glColor4fv(self.color)
        glPushMatrix()
        glTranslatef(self._translate.x, self._translate.y, 0)
        glRectf(*(self.top_left & self.bottom_right))
        glPopMatrix()

    def motion(self, x, y):
        if not self.done:
            # Note that the sorting done in BaseGraphic__init__
            # is worth nothing...
            self.bottom_right = Point(x, y)
            
    def move(self, move_from, move_to):
        # make sure we can treat coordinates as Points
        move_from, move_to = map(Point._make, (move_from, move_to))
        
        # update translation vector
        self._translate += move_to - move_from


class Ellipse(BaseGraphic):
    def __init__(self, top_left, bottom_right):
        super(Ellipse, self).__init__(top_left, bottom_right)
        #self.color = glGetFloatv(GL_CURRENT_COLOR)
        self.color = (0.78, 0.78, 0.35, 1.0) # Force color
        self.done = False
        self.selected = False
        self._translate = Point(0, 0)

    def draw(self):
        quadratic = gluNewQuadric()
        if not self.done:
            # draw guides in the first and last corners
            r, g, b, a = self.color
            inverse_color = (1-r, 1-g, 1-b, a)
            glColor4fv(inverse_color)
            glPushMatrix()
            glTranslatef(self.top_left.x, self.top_left.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(self.bottom_right.x, self.bottom_right.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
        glColor4fv(self.color)
        glPushMatrix()
        radius = abs(self.top_left.x - self.bottom_right.x) / 2.0
        tr_x, tr_y = (self.top_left + self.bottom_right) / 2.0
        glTranslatef(tr_x, tr_y, 0)
        d_x, d_y = map(abs, (self.top_left - self.bottom_right))
        # Avoid division by zero
        d_x = d_x or 1
        glScale(1.0, 1.0 * d_y / d_x, 1.0)
        glTranslatef(self._translate.x, self._translate.y, 0)
        gluDisk(quadratic, 0, radius, d_x / 2, d_y / 2)
        glPopMatrix()

    def motion(self, x, y):
        if not self.done:
            # Note that the sorting done in BaseGraphic__init__
            # is worth nothing...
            self.bottom_right = Point(x, y)
            
    def move(self, move_from, move_to):
        # make sure we can treat coordinates as Points
        move_from, move_to = map(Point._make, (move_from, move_to))
        
        # update translation vector
        self._translate += move_to - move_from


class FreeForm(object):
    def __init__(self, start):
        self.points = [Point._make(start)]
        #self.color = glGetFloatv(GL_CURRENT_COLOR)
        self.color = (0.68, 0.68, 0.54, 1.0) # Force color
        self.done = False
        self.selected = False
        self._translate = Point(0, 0)

    def __contains__(self, (x, y)):
        # TODO: implement properly
        return True

    def __repr__(self):
        if len(self.points) > 6:
            first_points = map(str, self.points[:3])
            last_points = map(str, self.points[-3:])
            repr_points = "[%s, ..., %s]" % tuple(map(", ".join, (first_points, last_points)))
        else:
            repr_points = str(self.points)
        return "<%s points=%s>" % (self.__class__.__name__, repr_points)

    def draw(self):
        start_point = self.points[0]
        end_point = self.points[-1]
        if not self.done:
            # draw guides in the first and last corners
            quadratic = gluNewQuadric()
            r, g, b, a = self.color
            inverse_color = (1-r, 1-g, 1-b, a)
            glColor4fv(inverse_color)
            glPushMatrix()
            glTranslatef(start_point.x, start_point.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(end_point.x, end_point.y, 0)
            gluDisk(quadratic, 0, 3, 32, 32)
            glPopMatrix()
        glColor4fv(self.color)
        glPushMatrix()
        glTranslatef(self._translate.x, self._translate.y, 0)
        glBegin(GL_LINE_STRIP)
        for point in self.points:
            glVertex2f(*point)
        glEnd()
        glPopMatrix()

    def motion(self, x, y):
        # Add new points to the FreeForm
        if not self.done:
            self.points.append(Point(x, y))
            
    def move(self, move_from, move_to):
        # make sure we can treat coordinates as Points
        move_from, move_to = map(Point._make, (move_from, move_to))
        
        # update translation vector
        self._translate += move_to - move_from
