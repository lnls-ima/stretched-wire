# -*- coding: utf-8 -*-
"""Stretched Wire application."""

import sys as _sys
import threading as _threading

from qtpy.QtWidgets import QApplication as _QApplication
from stretchedwire.gui.mainwindow import MainWindow as _MainWindow
from stretchedwire.data import meas as _meas
from stretchedwire.gui import utils as _utils
import stretchedwire.data as _data


class StretchedWireApp(_QApplication):
    """Stretched Wire GUI application."""

    def __init__(self, args):
        """Start application."""
        super().__init__(args)
        self.setStyle(_utils.WINDOW_STYLE)

        self.meas = _meas

        self.directory = _utils.BASEPATH
        self.database_name = _utils.DATABASE_NAME
        self.mongo = _utils.MONGO
        self.server = _utils.SERVER
        self.create_database()

    def create_database(self):
        """Create database and tables."""
        _Config = _data.configuration.StretchedWireConfig(
            database_name=self.database_name,
            mongo=self.mongo, server=self.server)
        _Meas = _data.measurement.StretchedWireMeas(
            database_name=self.database_name,
            mongo=self.mongo, server=self.server)
        _PowerSupplyConfig = _data.configuration.PowerSupplyConfig(
            database_name=self.database_name,
            mongo=self.mongo, server=self.server)

        status = []
        status.append(_Config.db_create_collection())
        status.append(_Meas.db_create_collection())
        status.append(_PowerSupplyConfig.db_create_collection())
        if not all(status):
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
        if (not _QApplication.instance()):
            print('oi')
            self.app = StretchedWireApp([])
            self.window = _MainWindow(
                width=_utils.WINDOW_WIDTH, height=_utils.WINDOW_HEIGHT)
            self.window.show()
            _sys.exit(self.app.exec_())


def run():
    """Run stretched wire GUI application."""
    app = None
    if not _QApplication.instance():
        app = StretchedWireApp([])
        window = _MainWindow(
            width=_utils.WINDOW_WIDTH, height=_utils.WINDOW_HEIGHT)
        window.show()
        _sys.exit(app.exec_())


def run_in_thread():
    """Run stretched wire GUI application in a thread."""
    return GUIThread()
