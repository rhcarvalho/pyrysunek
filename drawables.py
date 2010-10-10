# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import Point


class Drawable(object):

    """Represent a drawable OpenGL object.

    This class is intended to be subclassed.
    Subclasses must implement these methods/properties:
        @property centroid
        __contains__(self, (x, y))
        draw_construction_guides(self)
        draw_element(self)
        draw_selection_overlay(self)
        construct(self, x, y)

    These methods/properties are provided and may be used as-is by subclasses:
        @property highlight_color
        draw(self)
        draw_small_disk(self, point)
        draw_rectangle_outline(self, corner, opposite_corner)
        finish(self)
        @property finished
        move(self, from_point, to_point)
        resize(self, from_point, to_point)

    """

    def __init__(self):
        """You should not instantiate the class Drawable directly."""
        self.color = glGetFloatv(GL_CURRENT_COLOR)
        self._finished = False
        self.selected = False
        self.translation_vector = Point(0, 0)
        self.resize_vector = Point(1, 1)
        self.quadratic = gluNewQuadric()

    def __repr__(self):
        return "%s()" % (self.__class__.__name__,)

    def __contains__(self, (x, y)):
        """Return whether (x, y) is inside this drawable."""
        raise NotImplementedError

    @property
    def centroid(self):
        """Return current centroid of this object."""
        raise NotImplementedError

    @property
    def highlight_color(self):
        """Return a 4-value highlight color tuple."""
        r, g, b, a = self.color
        inverse_color = (1 - r, 1 - g, 1 - b, a)
        return inverse_color

    def draw_construction_guides(self):
        """Draw elements specific to drawable interactive creation."""
        raise NotImplementedError

    def draw_element(self):
        """Draw main drawable object."""
        raise NotImplementedError

    def draw_selection_overlay(self):
        """Draw elements specific to drawable selection."""
        raise NotImplementedError

    def draw(self):
        """Draw this drawable as a whole.

        This method interact with `draw_construction_guides`, `draw_element`
        and `draw_selection_overlay` to draw itself.
        It ensures that the OpenGL transformation matrix will be untouched.
        It set the colors of the construction guides and selection overlay
        to the `highlight_color`, and the main element to it's `color`.

        """
        glPushMatrix()

        if not self.finished:
            glColor4fv(self.highlight_color)
            self.draw_construction_guides()

        glColor4fv(self.color)
        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0)
        glPushMatrix()
        self.draw_element()
        glPopMatrix()
        glColor4fv((0.6, 0.0, 0.0, 0.0))
        self.draw_small_disk(self.centroid)

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

    def construct(self, x, y):
        """Construct this object given mouse position (x, y)."""
        raise NotImplementedError

    def finish(self):
        """Finish construction of this object.

        Once called, this object won't respond to calls to `construct` anymore.

        """
        self._finished = True

    @property
    def finished(self):
        return self._finished

    def move(self, from_point, to_point):
        """Move this object relative to two points.

        This method can be called from external code, so that `from_point` and
        `to_point` need NOT to be Point instances. (x, y) tuples work as well.

        """
        # Make sure we can treat coordinates as Point instances.
        from_point, to_point = map(Point._make, (from_point, to_point))

        # Update translation vector.
        self.translation_vector += to_point - from_point

    def resize(self, from_point, to_point):
        """Resize this object relative to two points.

        This method can be called from external code, so that `from_point` and
        `to_point` need NOT to be Point instances. (x, y) tuples work as well.

        """
        # Make sure we can treat coordinates as Point instances.
        from_point, to_point = map(Point._make, (from_point, to_point))

        initial_distance = (from_point - self.centroid).hypot
        final_distance = (to_point - self.centroid).hypot
        if initial_distance != 0:
            # Update resize vector.
            self.resize_vector *= final_distance / initial_distance



class Rectangle(Drawable):
    def __init__(self, corner1, corner2):
        super(Rectangle, self).__init__()
        self.corner1, self.corner2 = map(Point._make, (corner1, corner2))
        self.color = (0.08, 0.08, 0.54, 1.0) # Force color

    def __contains__(self, (x, y)):
        # Take into account `translation_vector`.
        corner1 = self.corner1 + self.translation_vector
        corner2 = self.corner2 + self.translation_vector
        # Check whether (x, y) is inside the boundaries.
        x_is_in_boundary = sorted((corner1.x, x, corner2.x))[1] == x
        y_is_in_boundary = sorted((corner1.y, y, corner2.y))[1] == y
        return x_is_in_boundary and y_is_in_boundary

    @property
    def centroid(self):
        return (self.corner1 + self.corner2) / 2.0

    def draw_construction_guides(self):
        # Draw guides in the first and last corners.
        self.draw_small_disk(self.corner1)
        self.draw_small_disk(self.corner2)

    def draw_element(self):
        glRectf(*(self.corner1 & self.corner2))

    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.corner1, self.corner2)

    def construct(self, x, y):
        # Update the second corner position.
        if not self.finished:
            self.corner2 = Point(x, y)


class Ellipse(Drawable):
    def __init__(self, corner1, corner2):
        super(Ellipse, self).__init__()
        self.corner1, self.corner2 = map(Point._make, (corner1, corner2))
        self.color = (0.78, 0.78, 0.35, 1.0) # Force color

    def __contains__(self, (x, y)):
        # Take into account `translation_vector`.
        corner1 = self.corner1 + self.translation_vector
        corner2 = self.corner2 + self.translation_vector

        # Compute ellipse parameters.
        a, b = (corner1 - corner2) / 2.0

        # Compute coordinates of the center.
        xc, yc = (corner1 + corner2) / 2.0

        # Compute ellipse function with 2 decimal digits precision.
        fx = round((((x - xc) ** 2.0) / (a ** 2.0)) +
                   (((y - yc) ** 2.0) / (b ** 2.0)) - 1, 2)

        # (x, y) is inside of the ellipse if fx < 0, or in the border if fx == 0
        return fx <= 0.01

    @property
    def centroid(self):
        return (self.corner1 + self.corner2) / 2.0

    def draw_construction_guides(self):
        # Draw guides in the first and last corners.
        self.draw_small_disk(self.corner1)
        self.draw_small_disk(self.corner2)

    def draw_element(self):
        radius = abs(self.corner1.x - self.corner2.x) / 2.0
        tr_x, tr_y = (self.corner1 + self.corner2) / 2.0
        glTranslatef(tr_x, tr_y, 0)
        d_x, d_y = map(abs, (self.corner1 - self.corner2))
        # Avoid division by zero.
        d_x = d_x or 1
        glScale(1.0, 1.0 * d_y / d_x, 1.0)
        gluDisk(self.quadratic, 0, radius, d_x / 2, d_y / 2)

    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.corner1, self.corner2)

    def construct(self, x, y):
        # Update the second corner position.
        if not self.finished:
            self.corner2 = Point(x, y)


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
            # Take into account `translation_vector`.
            p1 = p1 + self.translation_vector
            p2 = p2 + self.translation_vector

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

    @property
    def centroid(self):
        return sum(self.points, Point(0, 0)) / float(len(self.points))

    def __repr__(self):
        if len(self.points) > 6:
            first_points = map(str, self.points[:3])
            last_points = map(str, self.points[-3:])
            repr_points = "[%s, ..., %s]" % tuple(map(", ".join, (first_points, last_points)))
        else:
            repr_points = str(self.points)
        return "%s(points=%s)" % (self.__class__.__name__, repr_points)

    def draw_construction_guides(self):
        # Draw guides in the first and last points.
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

    def construct(self, x, y):
        # Add new points to the FreeForm.
        if not self.finished:
            self.points.append(Point(x, y))
