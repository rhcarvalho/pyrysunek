# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import Point


class Drawable(object):
    def __init__(self):
        self.color = glGetFloatv(GL_CURRENT_COLOR)
        self.done = False
        self.selected = False
        self.translation_vector = Point(0, 0)
        self.quadratic = gluNewQuadric()

    def __repr__(self):
        return "%s(...)" % (self.__class__.__name__,)
        
    @property
    def highlight_color(self):
        r, g, b, a = self.color
        inverse_color = (1 - r, 1 - g, 1 - b, a)
        return inverse_color
        
    def draw(self):
        glPushMatrix()
        self.draw_construction_guides()
        self.draw_element()
        self.draw_selection_overlay()
        glPopMatrix()
        
    def draw_construction_guides(self):
        if not self.done:
            # draw guides in the first and last corners
            glColor4fv(self.highlight_color)
            glPushMatrix()
            glTranslatef(self.top_left.x, self.top_left.y, 0)
            gluDisk(self.quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(self.bottom_right.x, self.bottom_right.y, 0)
            gluDisk(self.quadratic, 0, 3, 32, 32)
            glPopMatrix()
        
    def draw_element(self):
        pass
        
    def draw_selection_overlay(self):
        if self.selected:
            glColor4fv(self.highlight_color)
            glBegin(GL_LINE_LOOP)
            glVertex2f(self.top_left.x, self.bottom_right.y)
            glVertex2f(self.bottom_right.x, self.bottom_right.y)
            glVertex2f(self.bottom_right.x, self.top_left.y)
            glVertex2f(self.top_left.x, self.top_left.y)
            glEnd()
    
    def move(self, move_from, move_to):
        # make sure we can treat coordinates as Points
        move_from, move_to = map(Point._make, (move_from, move_to))
        
        # update translation vector
        self.translation_vector += move_to - move_from
    

class Rectangle(Drawable):
    def __init__(self, top_left, bottom_right):
        super(Rectangle, self).__init__()
        self.top_left, self.bottom_right = map(Point._make, (top_left, bottom_right))
        self.color = (0.08, 0.08, 0.54, 1.0) # Force color

    def __contains__(self, (x, y)):
        return (self.top_left.x <= x < self.bottom_right.x) and (self.top_left.y <= y < self.bottom_right.y)

    def draw_element(self):
        glColor4fv(self.color)
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        glRectf(*(self.top_left & self.bottom_right))

    def motion(self, x, y):
        if not self.done:
            self.bottom_right = Point(x, y)


class Ellipse(Drawable):
    def __init__(self, top_left, bottom_right):
        super(Ellipse, self).__init__()
        self.top_left, self.bottom_right = map(Point._make, (top_left, bottom_right))
        self.color = (0.78, 0.78, 0.35, 1.0) # Force color

    def __contains__(self, (x, y)):
        # TODO: implement properly
        return (self.top_left.x <= x < self.bottom_right.x) and (self.top_left.y <= y < self.bottom_right.y)

    def draw_element(self):
        glColor4fv(self.color)
        radius = abs(self.top_left.x - self.bottom_right.x) / 2.0
        tr_x, tr_y = (self.top_left + self.bottom_right) / 2.0
        glTranslatef(tr_x, tr_y, 0)
        d_x, d_y = map(abs, (self.top_left - self.bottom_right))
        # Avoid division by zero
        d_x = d_x or 1
        glScale(1.0, 1.0 * d_y / d_x, 1.0)
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        gluDisk(self.quadratic, 0, radius, d_x / 2, d_y / 2)

    def draw_selection_overlay(self):
        # BUG: selection overlay inconsistent when moving object.
        glPopMatrix()
        glPushMatrix()
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        super(Ellipse, self).draw_selection_overlay()

    def motion(self, x, y):
        if not self.done:
            self.bottom_right = Point(x, y)


class FreeForm(Drawable):
    def __init__(self, start):
        super(FreeForm, self).__init__()
        self.points = [Point._make(start)]
        self.color = (0.68, 0.68, 0.54, 1.0) # Force color

    def __contains__(self, (x, y)):
        # TODO: implement properly
        start_point = self.points[0]
        end_point = self.points[-1]
        p = Point(x, y)
        return (p - start_point).hypot < 10 or (p - end_point).hypot < 10

    def __repr__(self):
        if len(self.points) > 6:
            first_points = map(str, self.points[:3])
            last_points = map(str, self.points[-3:])
            repr_points = "[%s, ..., %s]" % tuple(map(", ".join, (first_points, last_points)))
        else:
            repr_points = str(self.points)
        return "%s(points=%s)" % (self.__class__.__name__, repr_points)
        
    @property
    def top_left(self):
        return self.points[0]
        
    @property
    def bottom_right(self):
        return self.points[-1]
        
    def draw_construction_guides(self):
        start_point = self.points[0]
        end_point = self.points[-1]
        if not self.done:
            # draw guides in the first and last corners
            glColor4fv(self.highlight_color)
            glPushMatrix()
            glTranslatef(start_point.x, start_point.y, 0)
            gluDisk(self.quadratic, 0, 3, 32, 32)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(end_point.x, end_point.y, 0)
            gluDisk(self.quadratic, 0, 3, 32, 32)
            glPopMatrix()

    def draw_element(self):
        start_point = self.points[0]
        end_point = self.points[-1]
        glColor4fv(self.color)
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        glBegin(GL_LINE_STRIP)
        for point in self.points:
            glVertex2f(*point)
        glEnd()

    def motion(self, x, y):
        # Add new points to the FreeForm
        if not self.done:
            self.points.append(Point(x, y))
