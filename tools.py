# -*- coding: utf-8 -*-

from drawables import *


class Tool(object):
    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def mouse_down(self, x, y, context):
        pass

    def mouse_up(self, x, y, context):
        pass

    def mouse_move(self, x, y, context):
        pass


class SelectionTool(Tool):
    def mouse_up(self, x, y, context):
        context.objects.select(x, y)


class RectangleTool(Tool):
    def mouse_down(self, x, y, context):
        context.objects.append(Rectangle((x, y), (x, y)))

    def mouse_up(self, x, y, context):
        if context.objects:
            # Mark last object as finished
            context.objects[-1].finish()

    def mouse_move(self, x, y, context):
        if context.objects:
            # update last object
            context.objects[-1].construct(x, y)


class EllipseTool(Tool):
    def mouse_down(self, x, y, context):
        context.objects.append(Ellipse((x, y), (x, y)))

    def mouse_up(self, x, y, context):
        if context.objects:
            # Mark last object as finished
            context.objects[-1].finish()

    def mouse_move(self, x, y, context):
        if context.objects:
            # update last object
            context.objects[-1].construct(x, y)

class FreeFormTool(Tool):
    def mouse_down(self, x, y, context):
        context.objects.append(FreeForm((x, y)))

    def mouse_up(self, x, y, context):
        if context.objects:
            # Mark last object as finished
            context.objects[-1].finish()

    def mouse_move(self, x, y, context):
        if context.objects:
            # update last object
            context.objects[-1].construct(x, y)

class ResizeTool(Tool):
    def mouse_down(self, x, y, context):
        # set initial position (x, y)
        pass

    def mouse_up(self, x, y, context):
        # clear initial position
        pass

    def mouse_move(self, x, y, context):
        # scale object by (initx, inity) -> (x, y)
        pass

class MoveTool(Tool):
    def mouse_down(self, x, y, context):
        # select object under cursor if there is no selection
        if not context.objects.selected:
            context.objects.select(x, y)
        # set initial position (x, y)
        context.move_from = (x, y)

    def mouse_up(self, x, y, context):
        # clear initial position
        del context.move_from

    def mouse_move(self, x, y, context):
        # translate object by (initial x, initial y) -> (x, y)
        if context.objects.selected and context.move_from:
            context.objects.selected.move(context.move_from, (x, y))
            context.move_from = (x, y)

class DeleteTool(Tool):
    def mouse_up(self, x, y, context):
        # delete object under current position
        pass
