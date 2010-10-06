# -*- coding: utf-8 -*-

class Tool(object):
    def __repr__(self):
        return "<%s>" % self.__class__.__name__

class SelectionTool(Tool):
    pass

class RectangleTool(Tool):
    pass

class EllipseTool(Tool):
    pass

class LineTool(Tool):
    pass

class ResizeTool(Tool):
    pass

class MoveTool(Tool):
    pass

class DeleteTool(Tool):
    pass
