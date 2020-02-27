# -*- coding: utf-8 -*-

"""General functions that can be used in more than on widget."""

import os.path as _path
from qtpy.QtGui import (
    QFont as _QFont,
    )
from qtpy.QtCore import QSize as _QSize

_basepath = _path.dirname(__file__)

# GUI configurations
WINDOW_STYLE = 'windows'
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FONT_SIZE = 11
ICON_SIZE = 24
DATABASE_NAME = 'stretched_wire_measurements.db'
MONGO = False
SERVER = 'localhost'
UPDATE_POSITIONS_INTERVAL = 0.5  # [s]
UPDATE_PLOT_INTERVAL = 0.1  # [s]
TABLE_NUMBER_ROWS = 1000
TABLE_MAX_NUMBER_ROWS = 100
TABLE_MAX_STR_SIZE = 100


BASEPATH = _path.dirname(
    _path.dirname(_path.dirname(_path.abspath(__file__))))
if not MONGO:
    DATABASE_NAME = _path.join(BASEPATH, DATABASE_NAME)


def get_default_font(bold=False):
    """Return the default QFont."""
    font = _QFont()
    font.setPointSize(FONT_SIZE)
    font.setBold(bold)
    return font


def get_default_icon_size():
    """Return the default QSize for icons."""
    return _QSize(ICON_SIZE, ICON_SIZE)


def get_icon_path(icon_name):
    """Get the icon file path."""
    img_path = _path.join(
        _path.join(_path.dirname(_basepath), 'resources'), 'img')
    icon_path = _path.join(img_path, '{0:s}.png'.format(icon_name))
    icon_path = icon_path.replace('\\', '/')
    return icon_path


def get_ui_file(widget):
    """Get the ui file path."""
    if isinstance(widget, type):
        basename = '{0:s}.ui'.format(widget.__name__.lower())
    else:
        basename = '{0:s}.ui'.format(widget.__class__.__name__.lower())
    uifile = _path.join(_basepath, _path.join('ui', basename))
    return uifile
