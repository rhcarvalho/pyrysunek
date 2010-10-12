# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import Point


class Drawable(object):

    """Represent a drawable OpenGL object.

    This class is intended to be subclassed.
    Subclasses must implement these methods/properties:
        normalize(self)
        @property centroid
        __contains__(self, (x, y))
        draw_construction_guides(self)
        draw_fill(self)
        draw_outline(self)
        draw_selection_overlay(self)
        construct(self, x, y)

    These methods/properties are provided and may be used as-is by subclasses:
        denormalized(self, point)
        @property highlight_color
        draw(self)
        draw_small_disk(self, point)
        draw_rectangle_outline(self, corner, opposite_corner)
        finish(self)
        @property finished
        move(self, from_point, to_point)
        resize(self, from_point, to_point)

    """

    def __init__(self, fill_color, line_color):
        """You should not instantiate the class Drawable directly."""
        self.fill_color = fill_color
        self.line_color = line_color
        self._finished = False
        self.selected = False
        self.translation_vector = Point(0, 0)
        self.resize_vector = Point(1, 1)

    def __repr__(self):
        return "%s()" % (self.__class__.__name__,)

    def __contains__(self, (x, y)):
        """Return whether (x, y) is inside this drawable."""
        raise NotImplementedError

    @property
    def centroid(self):
        """Return current centroid of this object."""
        raise NotImplementedError

    def normalize(self):
        """"Normalize control points of this object.

        All of the control points will be translated so that the object's
        centroid lies in the center of the coordinate system (0, 0).

        """
        raise NotImplementedError

    def denormalized(self, point):
        """"Return denormalized coordinates for `point`.

        The denormalized coordinates are computed by applying the
        `resize_vector` and `translation_vector`.

        """
        x, y = point

        # Take into account `resize_vector`.
        x *= self.resize_vector.x
        y *= self.resize_vector.y
        denormalized_point = Point(x, y)

        # Take into account `translation_vector`.
        denormalized_point += self.translation_vector

        return denormalized_point

    @property
    def highlight_color(self):
        """Return a 4-value highlight color tuple."""
        # Average fill color and line color.
        combined_color = map(lambda (x, y): (x + y) / 2.0,
                             zip(self.fill_color, self.line_color))
        # Invert combined color.
        r, g, b, a = combined_color
        highlight_color = (1 - r, 1 - g, 1 - b, a)
        return highlight_color

    def draw_construction_guides(self):
        """Draw elements specific to drawable interactive creation."""
        raise NotImplementedError

    def draw_fill(self):
        """Draw main drawable object."""
        raise NotImplementedError

    def draw_outline(self):
        """Draw outline of main drawable object."""
        raise NotImplementedError

    def draw_selection_overlay(self):
        """Draw elements specific to drawable selection."""
        raise NotImplementedError

    def draw(self):
        """Draw this drawable as a whole.

        This method interact with `draw_construction_guides`, `draw_fill`,
        `draw_outline` and `draw_selection_overlay` to draw itself.
        It ensures that the OpenGL transformation matrix will be untouched.
        It set the colors of the construction guides and selection overlay
        to the `highlight_color`, and the main element to its `fill_color`
        and `line_color`.

        """
        glPushMatrix()

        if not self.finished:
            glColor4fv(self.highlight_color)
            self.draw_construction_guides()

        glTranslatef(self.translation_vector.x, self.translation_vector.y, 0.0)
        glScale(self.resize_vector.x, self.resize_vector.y, 1.0)

        glPushMatrix()
        glColor4fv(self.line_color)
        # Draw outline first so that it is possible to simulate the outline
        # effect by drawing overlapping filled objects.
        self.draw_outline()
        glPopMatrix()
        glPushMatrix()
        glColor4fv(self.fill_color)
        self.draw_fill()
        glPopMatrix()

        if self.selected:
            glColor4fv(self.highlight_color)
            self.draw_selection_overlay()

        glPopMatrix()

    def draw_small_disk(self, point):
        """Helper method to draw a small disk centered in the given point."""
        glPushMatrix()
        glTranslatef(point.x, point.y, 0)
        gluDisk(gluNewQuadric(), 0, 3, 32, 32)
        glPopMatrix()

    def draw_rectangle_outline(self, corner, opposite_corner, radial_reduction):
        """Helper method to draw a rectangle outline given two opposite corners."""
        x1, y1, x2, y2 = corner & opposite_corner

        # Make sure x1 <= x2 and y1 <= y2.
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        # Contract boundaries by `radial_reduction`.
        #x1 += radial_reduction
        x2 -= radial_reduction
        #y1 += radial_reduction
        y2 -= radial_reduction

        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, y2)
        glVertex2f(x2, y2)
        glVertex2f(x2, y1)
        glVertex2f(x1, y1)
        glEnd()

    def construct(self, x, y):
        """Construct this object given mouse position (x, y)."""
        raise NotImplementedError

    def finish(self):
        """Finish construction of this object.

        Once called, this object won't respond to calls to `construct` anymore.
        Also, all of its control points will be normalized.

        """
        self._finished = True
        self.normalize()

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

        scale_x, scale_y = self.resize_vector
        from_vector = from_point - self.translation_vector
        to_vector = to_point - self.translation_vector

        # Avoid division by zero.
        from_vector += Point(0.001, 0.001)

        # Update scale.
        scale_x *= to_vector.x / from_vector.x
        scale_y *= to_vector.y / from_vector.y

        self.resize_vector = Point(scale_x, scale_y)


class Rectangle(Drawable):
    def __init__(self, fill_color, line_color, corner1, corner2):
        super(Rectangle, self).__init__(fill_color, line_color)
        self.corner1, self.corner2 = map(Point._make, (corner1, corner2))

    def __contains__(self, (x, y)):
        corner1 = self.denormalized(self.corner1)
        corner2 = self.denormalized(self.corner2)

        # Check whether (x, y) is inside the boundaries.
        x_is_in_boundary = sorted((corner1.x, x, corner2.x))[1] == x
        y_is_in_boundary = sorted((corner1.y, y, corner2.y))[1] == y
        return x_is_in_boundary and y_is_in_boundary

    @property
    def centroid(self):
        return (self.corner1 + self.corner2) / 2.0

    def normalize(self):
        centroid = self.centroid
        self.translation_vector += centroid
        self.corner1 -= centroid
        self.corner2 -= centroid

    def draw_construction_guides(self):
        # Draw guides in the first and last corners.
        self.draw_small_disk(self.corner1)
        self.draw_small_disk(self.corner2)

    def _draw_rectangle(self, radial_reduction):
        x1, y1, x2, y2 = self.corner1 & self.corner2

        # Make sure x1 <= x2 and y1 <= y2.
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        # Contract boundaries by `radial_reduction`.
        x1 += radial_reduction
        x2 -= radial_reduction
        y1 += radial_reduction
        y2 -= radial_reduction

        # Draw rectangle.
        glRectf(x1, y1, x2, y2)

    def draw_fill(self):
        self._draw_rectangle(1.0)

    def draw_outline(self):
        self._draw_rectangle(0.0)

    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.corner1, self.corner2, -1.0)

    def construct(self, x, y):
        # Update the second corner position.
        if not self.finished:
            self.corner2 = Point(x, y)


class Ellipse(Drawable):
    def __init__(self, fill_color, line_color, corner1, corner2):
        super(Ellipse, self).__init__(fill_color, line_color)
        self.corner1, self.corner2 = map(Point._make, (corner1, corner2))

    def __contains__(self, (x, y)):
        corner1 = self.denormalized(self.corner1)
        corner2 = self.denormalized(self.corner2)

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

    def normalize(self):
        centroid = self.centroid
        self.translation_vector += centroid
        self.corner1 -= centroid
        self.corner2 -= centroid

    def draw_construction_guides(self):
        # Draw guides in the first and last corners.
        self.draw_small_disk(self.corner1)
        self.draw_small_disk(self.corner2)

    def _draw_ellipse(self, radial_reduction):
        # Compute radius from the x coordinate.
        radius = abs(self.corner1.x - self.corner2.x) / 2.0 - radial_reduction

        # Center the ellipse on its centroid.
        tr_x, tr_y = self.centroid
        glTranslatef(tr_x, tr_y, 0.0)

        # Scale to transform disk into ellipse.
        d_x, d_y = map(lambda x: float(abs(x)), (self.corner1 - self.corner2))
        # Avoid division by zero.
        d_x = d_x or 1.0
        glScale(1.0, d_y / d_x, 1.0)

        # Draw filled disk/ellipse.
        gluDisk(gluNewQuadric(), 0.0, radius, int(d_x / 2.0), int(d_y / 2.0))

    def draw_fill(self):
        self._draw_ellipse(1.0)

    def draw_outline(self):
        self._draw_ellipse(0.0)

    def draw_selection_overlay(self):
        self.draw_rectangle_outline(self.corner1, self.corner2, -1.0)

    def construct(self, x, y):
        # Update the second corner position.
        if not self.finished:
            self.corner2 = Point(x, y)


class FreeForm(Drawable):
    def __init__(self, fill_color, line_color, start):
        super(FreeForm, self).__init__(fill_color, line_color)
        self.points = [Point._make(start)]

    def __contains__(self, (x, y)):
        """Test whether (x, y) is close enough to this free form.

        In other words, that the minimum distance between (x, y) and one of the
        line segments of this free form is smaller than a threshold.

        """
        threshold = 3
        q = Point(x, y)
        # Iterate over all pairs of sequential points.
        for p1, p2 in zip(self.points, self.points[1:]):
            p1 = self.denormalized(p1)
            p2 = self.denormalized(p2)

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

    def normalize(self):
        centroid = self.centroid
        self.translation_vector += centroid
        for i in xrange(len(self.points)):
            self.points[i] -= centroid

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

    def draw_fill(self):
        pass

    def draw_outline(self):
        glBegin(GL_LINE_STRIP)
        for point in self.points:
            glVertex2f(*point)
        glEnd()

    def draw_selection_overlay(self):
        top_left = Point(min(p.x for p in self.points),
                         min(p.y for p in self.points))
        bottom_right = Point(max(p.x for p in self.points),
                             max(p.y for p in self.points))
        self.draw_rectangle_outline(top_left, bottom_right, -1.0)

    def construct(self, x, y):
        # Add new points to the FreeForm.
        if not self.finished:
            self.points.append(Point(x, y))
