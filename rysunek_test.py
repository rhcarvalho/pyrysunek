import unittest
import rysunek
from OpenGL.GLUT import *


class TestToolbar(unittest.TestCase):
    def testActivateTool(self):
        app = rysunek.App()
        toolbar = app.getToolbar()
        tools = {
            (0, 0): toolbar.SELECTION_TOOL,
            (65, 0): toolbar.RECTANGLE_TOOL,
            (129, 0): toolbar.ELLIPSE_TOOL,
            (193, 0): toolbar.LINE_TOOL,
            (289, 0): toolbar.RESIZE_TOOL,
            (353, 0): toolbar.MOVE_TOOL,
            (417, 0): toolbar.DELETE_TOOL,
        }
        for coord, tool in tools.iteritems():
            app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, *coord)
            selectedTool = toolbar.getSelectedTool()
            self.assertEqual(selectedTool, tool)


class RectangleTest(unittest.TestCase):
    def testCannotCreateEmptyRectangle(self):
        app = rysunek.App()
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_DOWN, 0, 0) # click
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, 0, 0) # release
        self.assertEqual(len(app.getObjects()), 0)
        
    def testCanCreateSimpleRectangle(self):
        app = rysunek.App()
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_DOWN, 0, 0) # click
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, 10, 10) # release
        self.assertEqual(len(app.getObjects()), 1)
        
    def testCanCreateTwoRectangles(self):
        app = rysunek.App()
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_DOWN, 10, 10) # click
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, 20, 30) # release
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_DOWN, 40, 40) # click
        app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, 50, 60) # release
        self.assertEqual(len(app.getObjects()), 2)


if __name__ == "__main__":
    unittest.main()