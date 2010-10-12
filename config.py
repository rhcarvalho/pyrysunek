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
        color = (0.90625, 0.90625, 0.890625, 1.0),
        selection_color = (0.82, 0.82, 0.95, 1.0),
        color_picker = Config(
            default_fill_color = (0.0, 0.0, 0.0, 1.0),
            default_line_color = (1.0, 1.0, 0.0, 1.0),
            colors = (
                (0.0, 0.0, 0.0, 1.0),
                
                (1.0, 0.0, 0.0, 1.0),
                (0.0, 1.0, 0.0, 1.0),
                (0.0, 0.0, 1.0, 1.0),
                
                (1.0, 1.0, 1.0, 1.0),
                
                (1.0, 1.0, 0.0, 1.0),
                (0.0, 1.0, 1.0, 1.0),
                (1.0, 0.0, 1.0, 1.0),
            ),
        ),
    ),
    temp_file = "tmp.ryk",
    auto_load_on_start = True,
)
