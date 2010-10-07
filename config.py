# -*- coding: utf-8 -*-

# Default configuration for PyRysunek
__version__ = (0, 1)

class Config(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

default = Config(
    bg_color = (1.0, 1.0, 1.0, 1.0),
    window_size = (800, 500),
    window_position = (150, 50),
    window_title = "PyRysunek - v%s" % ".".join(map(str, __version__)),
    toolbar = Config(
        position = (0, 0), # top-left coordinate
        size = (800, 64),
    ),
)
