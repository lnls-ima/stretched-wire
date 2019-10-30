"""Stretched Wire package."""

import os as _os


_basedir = _os.path.dirname(__file__)
with open(_os.path.join(_basedir, 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()
