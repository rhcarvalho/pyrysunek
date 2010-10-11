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
        color = context.color_picker.current_fill_color
        context.objects.append(Rectangle(color, (x, y), (x, y)))

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
        color = context.color_picker.current_fill_color
        context.objects.append(Ellipse(color, (x, y), (x, y)))

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
        color = context.color_picker.current_fill_color
        context.objects.append(FreeForm(color, (x, y)))

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
        # select object under cursor if there is no selection
        if not context.objects.selected:
            context.objects.select(x, y)
        # set initial position (x, y)
        context.resize_from = (x, y)

    def mouse_up(self, x, y, context):
        # clear initial position
        del context.resize_from

    def mouse_move(self, x, y, context):
        # scale object by (initial x, initial y) -> (x, y)
        if context.objects.selected and context.resize_from:
            context.objects.selected.resize(context.resize_from, (x, y))
            context.resize_from = (x, y)


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
        context.objects.select(x, y)
        if context.objects.selected:
            context.objects.remove(context.objects.selected)
            context.objects.selected = None
