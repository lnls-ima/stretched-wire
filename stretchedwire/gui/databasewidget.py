# -*- coding: utf-8 -*-
"""Database Widget."""

import os as _os
import sys as _sys
import traceback as _traceback
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QApplication as _QApplication,
    QMessageBox as _QMessageBox,
    QFileDialog as _QFileDialog,
    )
import qtpy.uic as _uic

from imautils.gui import databasewidgets as _databasewidgets
from stretchedwire.gui.utils import get_ui_file as _get_ui_file

import stretchedwire.data as _data


_PowerSupplyConfig = _data.configuration.PowerSupplyConfig
_Config = _data.configuration.StretchedWireConfig
_Meas = _data.measurement.StretchedWireMeas


class DatabaseWidget(_QWidget):
    """Database Widget class."""

    _ps_table_name = _PowerSupplyConfig.collection_name
    _config_table_name = _Config.collection_name
    _meas_table_name = _Meas.collection_name

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self._table_object_dict = {
            self._ps_table_name: _PowerSupplyConfig,
            self._config_table_name: _Config,
            self._meas_table_name: _Meas,
            }

        self.twg_database = _databasewidgets.DatabaseTabWidget(
            database_name=self.database_name,
            mongo=self.mongo, server=self.server)
        self.ui.lyt_database.addWidget(self.twg_database)

        # connect signals and slots
        self.connect_signal_slots()

    @property
    def database_name(self):
        """Database name."""
        return _QApplication.instance().database_name

    @property
    def mongo(self):
        """MongoDB database."""
        return _QApplication.instance().mongo

    @property
    def server(self):
        """Server for MongoDB database."""
        return _QApplication.instance().server

    @property
    def directory(self):
        """Return the default directory."""
        return _QApplication.instance().directory

    def clear(self):
        """Clear."""
        try:
            self.twg_database.delete_widgets()
            self.twg_database.clear()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.tbt_refresh.clicked.connect(self.update_database_tables)
        self.ui.tbt_clear.clicked.connect(self.clear)
        self.ui.pbt_save.clicked.connect(self.save_files)
        self.ui.pbt_read.clicked.connect(self.read_files)
        self.ui.pbt_delete.clicked.connect(
            self.twg_database.delete_database_documents)

    def save_files(self):
        """Save database record to file."""
        try:
            table_name = self.twg_database.get_current_table_name()
            if table_name is None:
                return

            object_class = self._table_object_dict[table_name]

            idns = self.twg_database.get_table_selected_ids(table_name)
            nr_idns = len(idns)
            if nr_idns == 0:
                return

            objs = []
            fns = []
            try:
                for i in range(nr_idns):
                    idn = idns[i]
                    obj = object_class(
                        database_name=self.database_name,
                        mongo=self.mongo, server=self.server)
                    obj.db_read(idn)
                    default_filename = obj.default_filename
                    objs.append(obj)
                    fns.append(default_filename)

            except Exception:
                _traceback.print_exc(file=_sys.stdout)
                msg = 'Failed to read database entries.'
                _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)
                return

            if nr_idns == 1:
                filename = _QFileDialog.getSaveFileName(
                    self, caption='Save file',
                    directory=_os.path.join(self.directory, fns[0]),
                    filter="Text files (*.txt *.dat)")

                if isinstance(filename, tuple):
                    filename = filename[0]

                if len(filename) == 0:
                    return

                fns[0] = filename
            else:
                directory = _QFileDialog.getExistingDirectory(
                    self, caption='Save files', directory=self.directory)

                if isinstance(directory, tuple):
                    directory = directory[0]

                if len(directory) == 0:
                    return

                for i in range(len(fns)):
                    fns[i] = _os.path.join(directory, fns[i])

            try:
                for i in range(nr_idns):
                    obj = objs[i]
                    idn = idns[i]
                    filename = fns[i]
                    if (not filename.endswith('.txt') and
                       not filename.endswith('.dat')):
                        filename = filename + '.txt'
                    obj.save_file(filename)
            except Exception:
                _traceback.print_exc(file=_sys.stdout)
                msg = 'Failed to save files.'
                _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)
        except Exception:
            _traceback.print_exc(file=_sys.stdout)

    def read_files(self):
        """Read file and save in database."""
        table_name = self.twg_database.get_current_table_name()
        if table_name is None:
            return

        object_class = self._table_object_dict[table_name]

        fns = _QFileDialog.getOpenFileNames(
            self, caption='Read files', directory=self.directory,
            filter="Text files (*.txt *.dat)")

        if isinstance(fns, tuple):
            fns = fns[0]

        if len(fns) == 0:
            return

        try:
            idns = []
            for filename in fns:
                obj = object_class(
                    database_name=self.database_name,
                    mongo=self.mongo, server=self.server)
                obj.read_file(filename)
                idn = obj.db_save()
                idns.append(idn)
            msg = 'Added to database table.\nIDs: ' + str(idns)
            self.update_database_tables()
            _QMessageBox.information(self, 'Information', msg, _QMessageBox.Ok)
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            msg = 'Failed to read files and save values in database.'
            _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)
            return

    def update_database_tables(self):
        """Update database tables."""
        if not self.isVisible():
            return

        try:
            self.twg_database.database_name = self.database_name
            self.twg_database.mongo = self.mongo
            self.twg_database.server = self.server
            self.twg_database.update_database_tables()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)

    def load_database(self):
        """Load database."""
        try:
            self.twg_database.database_name = self.database_name
            self.twg_database.mongo = self.mongo
            self.twg_database.server = self.server
            self.twg_database.load_database()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
