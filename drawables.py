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
        
    def __contains__(self, (x, y)):
        raise NotImplementedError
        
    @property
    def highlight_color(self):
        r, g, b, a = self.color
        inverse_color = (1 - r, 1 - g, 1 - b, a)
        return inverse_color
        
    def draw_construction_guides(self):
        raise NotImplementedError
        
    def draw_element(self):
        raise NotImplementedError
        
    def draw_selection_overlay(self):
        raise NotImplementedError
        
    def draw(self):
        glPushMatrix()
        
        if not self.done:
            glColor4fv(self.highlight_color)
            self.draw_construction_guides()
            
        glColor4fv(self.color)
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        glPushMatrix()
        self.draw_element()
        glPopMatrix()
        
        if self.selected:
            glColor4fv(self.highlight_color)
            self.draw_selection_overlay()
            
        glPopMatrix()
        
    def draw_small_disk(self, point):
        """Helper method to draw a small disk centered in the given point."""
        glPushMatrix()
        glTranslatef(point.x, point.y, 0)
        gluDisk(self.quadratic, 0, 3, 32, 32)
        glPopMatrix()
        
    def draw_rectangle_outline(self, corner, opposite_corner):
        """Helper method to draw a rectangle outline given two opposite corners."""
        glBegin(GL_LINE_LOOP)
        glVertex2f(corner.x, opposite_corner.y)
        glVertex2f(opposite_corner.x, opposite_corner.y)
        glVertex2f(opposite_corner.x, corner.y)
        glVertex2f(corner.x, corner.y)
        glEnd()
    
    def move(self, move_from, move_to):
        # make sure we can treat coordinates as Points
        move_from, move_to = map(Point._make, (move_from, move_to))
        
        # update translation vector
        self.translation_vector += move_to - move_from
        
    def motion(self, x, y):
        raise NotImplementedError
    
    

class Rectangle(Drawable):
    def __init__(self, top_left, bottom_right):
        super(Rectangle, self).__init__()
        self.top_left, self.bottom_right = map(Point._make, (top_left, bottom_right))
        self.color = (0.08, 0.08, 0.54, 1.0) # Force color

    def __contains__(self, (x, y)):
        # take into account translation_vector
        corner1 = self.top_left + self.translation_vector
        corner2 = self.bottom_right + self.translation_vector
        # check whether (x, y) is inside the boundaries
        return sorted((corner1.x, x, corner2.x))[1] == x and sorted((corner1.y, y, corner2.y))[1] == y
        
    def draw_construction_guides(self):
        # draw guides in the first and last corners
        self.draw_small_disk(self.top_left)
        self.draw_small_disk(self.bottom_right)

    def draw_element(self):
        glRectf(*(self.top_left & self.bottom_right))
        
    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.top_left, self.bottom_right)

    def motion(self, x, y):
        if not self.done:
            self.bottom_right = Point(x, y)


class Ellipse(Drawable):
    def __init__(self, top_left, bottom_right):
        super(Ellipse, self).__init__()
        self.top_left, self.bottom_right = map(Point._make, (top_left, bottom_right))
        self.color = (0.78, 0.78, 0.35, 1.0) # Force color

    def __contains__(self, (x, y)):
        # take into account translation_vector
        top_left = self.top_left + self.translation_vector
        bottom_right = self.bottom_right + self.translation_vector
        
        # Compute ellipse paramemters
        a, b = (top_left - bottom_right) / 2.0
        
        # Compute coordinates of the center
        xc, yc = (top_left + bottom_right) / 2.0
        
        # Compute ellipse function with 2 decimal digits precision
        fx = round((((x - xc) ** 2.0) / (a ** 2.0)) + (((y - yc) ** 2.0) / (b ** 2.0)) - 1, 2)
        
        # (x, y) is inside of the ellipse if fx < 0, or in the border if fx == 0
        return fx <= 0.01
        
    def draw_construction_guides(self):
        # draw guides in the first and last corners
        self.draw_small_disk(self.top_left)
        self.draw_small_disk(self.bottom_right)

    def draw_element(self):
        radius = abs(self.top_left.x - self.bottom_right.x) / 2.0
        tr_x, tr_y = (self.top_left + self.bottom_right) / 2.0
        glTranslatef(tr_x, tr_y, 0)
        d_x, d_y = map(abs, (self.top_left - self.bottom_right))
        # Avoid division by zero
        d_x = d_x or 1
        glScale(1.0, 1.0 * d_y / d_x, 1.0)
        gluDisk(self.quadratic, 0, radius, d_x / 2, d_y / 2)

    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.top_left, self.bottom_right)

    def motion(self, x, y):
        if not self.done:
            self.bottom_right = Point(x, y)


class FreeForm(Drawable):
    def __init__(self, start):
        super(FreeForm, self).__init__()
        self.points = [Point._make(start)]
        self.color = (0.68, 0.68, 0.54, 1.0) # Force color

    def __contains__(self, (x, y)):
        """Test whether (x, y) is close enough to this free form.
        In other words, that the minimum distance between (x, y) and one of the
        line segments of this free form is smaller than a threshold."""
        threshold = 3
        q = Point(x, y)
        # Iterate over all pairs of sequential points.
        for p1, p2 in zip(self.points, self.points[1:]):
            if p1 == p2:
                # If the points are coincident, then compute distance point-to-point.
                distance = (q - p1).hypot
            else:
                # Based on:
                # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/
                u = (
                    ((x - p1.x) * (p2.x - p1.x) + (y - p1.y)  * (p2.y - p1.y)) /
                    ((p2 - p1).hypot ** 2.0)
                )
                if 0 <= u <= 1:
                    # If the coeficient u is in the range 0..1, then the projection
                    # of q into the line defined by p1 and p2 lies inside the line
                    # segment defined by p1 and p2.
                    p = Point(p1.x + u * (p2.x - p1.x),
                              p1.y + u * (p2.y - p1.y))
                    distance = (p - q).hypot
                else:
                    # In this case, the minimum distance is that of q to p1 or p2.
                    distance = min((p1 - q).hypot, (p2 - q).hypot)
            
            if distance <= threshold:
                return True
        return False

    def __repr__(self):
        if len(self.points) > 6:
            first_points = map(str, self.points[:3])
            last_points = map(str, self.points[-3:])
            repr_points = "[%s, ..., %s]" % tuple(map(", ".join, (first_points, last_points)))
        else:
            repr_points = str(self.points)
        return "%s(points=%s)" % (self.__class__.__name__, repr_points)
        
    def draw_construction_guides(self):
        # draw guides in the first and last points
        self.draw_small_disk(self.points[0])
        self.draw_small_disk(self.points[-1])

    def draw_element(self):
        glBegin(GL_LINE_STRIP)
        for point in self.points:
            glVertex2f(*point)
        glEnd()
        
    def draw_selection_overlay(self):
        top_left = Point(min(p.x for p in self.points),
                         min(p.y for p in self.points))
        bottom_right = Point(max(p.x for p in self.points),
                             max(p.y for p in self.points))
        self.draw_rectangle_outline(top_left, bottom_right)

    def motion(self, x, y):
        # Add new points to the FreeForm
        if not self.done:
            self.points.append(Point(x, y))
