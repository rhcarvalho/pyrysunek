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
        icon_size = 32,
        padding = 5,
        color = (0.995, 0.995, 0.99, 1.0),
    ),
)
