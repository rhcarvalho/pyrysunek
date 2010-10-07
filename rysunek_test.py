import unittest
import rysunek
from geometry import Point
from OpenGL.GLUT import *


class TestToolbar(unittest.TestCase):
    def setUp(self):
        self.app = rysunek.App()

    def testDefaults(self):
        selected_tool = self.app.selected_tool
        line_size = self.app.line_size
        self.assertEqual(selected_tool, self.app.toolbar.SELECTION_TOOL)
        self.assertEqual(line_size, self.app.LINE_SIZE_THIN)

    def testActivateTool(self):
        tools = {
            (0, 0): self.app.toolbar.SELECTION_TOOL,
            (64, 0): self.app.toolbar.RECTANGLE_TOOL,
            (128, 0): self.app.toolbar.ELLIPSE_TOOL,
            (192, 0): self.app.toolbar.LINE_TOOL,
            (282, 0): self.app.toolbar.RESIZE_TOOL,
            (352, 0): self.app.toolbar.MOVE_TOOL,
            (416, 0): self.app.toolbar.DELETE_TOOL,
        }
        for coord, tool in tools.iteritems():
            self.app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, *coord)
            selected_tool = self.app.selected_tool
            self.assertEqual(selected_tool, tool)

    def testChangeLineSize(self):
        sizes = {
            0: self.app.LINE_SIZE_THIN,
            16: self.app.LINE_SIZE_MEDIUM,
            32: self.app.LINE_SIZE_LARGE,
            48: self.app.LINE_SIZE_XLARGE,
        }
        for y, size in sizes.iteritems():
            self.app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, 512, y)
            line_size = self.app.line_size
            self.assertEqual(line_size, size)


class RectangleTest(unittest.TestCase):
    def testCanCreateEmptyRectangle(self):
        app = rysunek.App()
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_DOWN, 80, 80) # click
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, 80, 80) # release
        self.assertEqual(len(app.getObjects()), 1)

    def testCanCreateSimpleRectangle(self):
        app = rysunek.App()
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_DOWN, 80, 80) # click
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, 90, 90) # release
        self.assertEqual(len(app.getObjects()), 1)

    def testCanCreateTwoRectangles(self):
        app = rysunek.App()
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_DOWN, 80, 80) # click
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, 90, 100) # release
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_DOWN, 110, 110) # click
        app.on_mouse_event(GLUT_LEFT_BUTTON, GLUT_UP, 120, 130) # release
        self.assertEqual(len(app.getObjects()), 2)


class PointTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(Point(4, 5) + Point(1, -3), Point(5, 2))
        self.assertEqual(Point(4, 5) - Point(1, -3), Point(3, 8))
        self.assertEqual((Point(4, 5) + Point(1, -3)) / 2.0, Point(2.5, 1.0))
        self.assertEqual(Point(4, 5) * 2.0, Point(8.0, 10.0))

    def test_comparison(self):
        self.assertTrue(Point(1, 1) < Point(2, 3))
        self.assertTrue(Point(10, 1) < Point(5, 9))
        self.assertTrue(Point(10, 5) > Point(5, 6))
        self.assertTrue(Point(1, 5) == Point(1, 5))
        self.assertTrue(Point(2, 5) != Point(1, 5))
        self.assertTrue(Point(1, 1) <= Point(1, 1))
        self.assertTrue(Point(0, 1) <= Point(1, 1))
        self.assertTrue(Point(5, 6) >= Point(5, 6))
        self.assertTrue(Point(10, 5) >= Point(5, 6))

    def test_aggregation(self):
        self.assertTrue(Point(4, 6) & Point(2, 3), (4, 6, 2, 3))


if __name__ == "__main__":
    unittest.main()