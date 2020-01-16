# -*- coding: utf-8 -*-
"""Stretched Wire application."""

import os as _os
import sys as _sys
import threading as _threading

from qtpy.QtWidgets import QApplication as _QApplication
from stretchedwire.gui.mainwindow import MainWindow as _MainWindow
from stretchedwire.data import meas as _meas

# Styles: ["windows", "motif", "cde", "plastique", "windowsxp", or "macintosh"]
_style = 'windows'
_width = 800
_height = 500
_database_filename = 'stretched_wire_measurements.db'


class StretchedWireApp(_QApplication):
    """Stretched Wire GUI application."""

    def __init__(self, args):
        """Start application."""
        super().__init__(args)
        self.setStyle(_style)

        self.meas = _meas

        self.directory = _os.path.dirname(_os.path.dirname(
            _os.path.dirname(_os.path.abspath(__file__))))
        self.meas.database_name = _os.path.join(
            self.directory, _database_filename)
        self.create_database()

    def create_database(self):
        """Create collections."""
        if not self.meas.create_collection():
            raise Exception("Failed to create database.")


class GUIThread(_threading.Thread):
    """GUI Thread."""

    def __init__(self):
        """Start thread."""
        _threading.Thread.__init__(self)
        self.app = None
        self.window = None
        self.daemon = True
        self.start()

    def run(self):
        """Thread target function."""
        if not _QApplication.instance():
            self.app = StretchedWireApp([])
            self.window = _MainWindow(width=_width, height=_height)
            self.window.show()
            _sys.exit(self.app.exec_())


def run():
    """Run stretched wire GUI application."""
    app = None
    if not _QApplication.instance():
        app = StretchedWireApp([])
        window = _MainWindow(width=_width, height=_height)
        window.show()
        _sys.exit(app.exec_())


def run_in_thread():
    """Run stretched wire GUI application in a thread."""
    return GUIThread()
