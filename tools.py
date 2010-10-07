# -*- coding: utf-8 -*-

from drawables import *


class Tool(object):
    def __repr__(self):
        return "<%s>" % self.__class__.__name__
        
    def mouse_down(self, x, y, objs):
        pass
    
    def mouse_up(self, x, y, objs):
        pass
    
    def mouse_move(self, x, y, objs):
        pass

class SelectionTool(Tool):
    pass


class RectangleTool(Tool):
    def mouse_down(self, x, y, objs):
        objs.append(Rectangle((x, y), (x, y)))
    
    def mouse_up(self, x, y, objs):
        if objs:
            # Mark last object as finished
            objs[-1].done = True
    
    def mouse_move(self, x, y, objs):
        if objs:
            # update last object
            objs[-1].motion(x, y)


class EllipseTool(Tool):
    def mouse_down(self, x, y, objs):
        objs.append(Ellipse((x, y), (x, y)))
    
    def mouse_up(self, x, y, objs):
        if objs:
            # Mark last object as finished
            objs[-1].done = True
    
    def mouse_move(self, x, y, objs):
        if objs:
            # update last object
            objs[-1].motion(x, y)

class FreeFormTool(Tool):
    def mouse_down(self, x, y, objs):
        objs.append(FreeForm((x, y)))
    
    def mouse_up(self, x, y, objs):
        if objs:
            # Mark last object as finished
            objs[-1].done = True
    
    def mouse_move(self, x, y, objs):
        if objs:
            # update last object
            objs[-1].motion(x, y)

class ResizeTool(Tool):
    pass

class MoveTool(Tool):
    pass

class DeleteTool(Tool):
    pass
