import unittest
import rysunek
from OpenGL.GLUT import *


class TestToolbar(unittest.TestCase):
    def setUp(self):
        self.app = rysunek.App()
        self.toolbar = self.app.getToolbar()

    def testActivateTool(self):
        tools = {
            (0, 0): self.toolbar.SELECTION_TOOL,
            (64, 0): self.toolbar.RECTANGLE_TOOL,
            (128, 0): self.toolbar.ELLIPSE_TOOL,
            (192, 0): self.toolbar.LINE_TOOL,
            (282, 0): self.toolbar.RESIZE_TOOL,
            (352, 0): self.toolbar.MOVE_TOOL,
            (416, 0): self.toolbar.DELETE_TOOL,
        }
        for coord, tool in tools.iteritems():
            self.app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, *coord)
            selectedTool = self.toolbar.getSelectedTool()
            self.assertEqual(selectedTool, tool)
            
    def testChangeLineSize(self):
        sizes = {
            0: self.app.LINE_SIZE_THIN,
            16: self.app.LINE_SIZE_MEDIUM,
            32: self.app.LINE_SIZE_LARGE,
            48: self.app.LINE_SIZE_XLARGE,
        }
        for y, size in sizes.iteritems():
            self.app.onMouseEvent(GLUT_LEFT_BUTTON, GLUT_UP, 512, y)
            currentLineSize = self.app.getLineSize()
            self.assertEqual(currentLineSize, size)

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