# -*- coding: utf-8 -*-
"""Database Widget."""

import os as _os
import sys as _sys
import numpy as _np
import traceback as _traceback
import sqlite3 as _sqlite
from qtpy.QtCore import Qt as _Qt
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QApplication as _QApplication,
    QLabel as _QLabel,
    QTableWidget as _QTableWidget,
    QTableWidgetItem as _QTableWidgetItem,
    QMessageBox as _QMessageBox,
    QVBoxLayout as _QVBoxLayout,
    QHBoxLayout as _QHBoxLayout,
    QSpinBox as _QSpinBox,
    QFileDialog as _QFileDialog,
    QAbstractItemView as _QAbstractItemView,
    )
import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file

from stretchedwire.data import config as _config
from stretchedwire.data import meas as _meas

_limit_number_rows = 1000
_max_number_rows = 100
_max_str_size = 100


class DatabaseWidget(_QWidget):
    """Database Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.config = _config
        self.meas = _meas

        self._tables = []
        self.ui.twg_database.clear()

        # connect signals and slots
        self.connect_signal_slots()

    @property
    def directory(self):
        """Return the default directory."""
        return _QApplication.instance().directory

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.tbt_refresh.clicked.connect(self.updateDatabaseTables)
        self.ui.tbt_clear.clicked.connect(self.clear)
        self.ui.pbt_save_to_file.clicked.connect(self.saveFiles)
#        self.ui.pbt_read.clicked.connect(self.read)
        self.ui.pbt_delete.clicked.connect(self.delete)

    def clear(self):
        """Clear."""
        try:
            ntabs = self.ui.twg_database.count()
            for idx in range(ntabs):
                self.ui.twg_database.removeTab(idx)
                self._tables[idx].deleteLater()
            self._tables = []
            self.ui.twg_database.clear()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)

    def saveFiles(self):
        """Save database record to file."""
        table_name = self.getCurrentTableName()
        if table_name is None:
            return

        idns = self.getTableSelectedIDs(table_name)
        nr_idns = len(idns)
        if nr_idns == 0:
            return

        objs = []
        fns = []
        try:
            for i in range(nr_idns):
                idn = idns[i]
                obj = self.meas
                default_filename = obj.default_filename
                if '.txt' in default_filename:
                    default_filename = default_filename.replace(
                        '.txt', '_ID={0:d}.txt'.format(idn))
                elif '.dat' in default_filename:
                    default_filename = default_filename.replace(
                        '.dat', '_ID={0:d}.dat'.format(idn))
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
                obj.db_read(idn)
                obj.save_file(filename)
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            msg = 'Failed to save files.'
            _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)

    def read(self):
        pass

    def delete(self):
        """Delete record from database table."""
        try:
            table_name = self.getCurrentTableName()
            if table_name is None:
                return

            idns = self.getTableSelectedIDs(table_name)
            if len(idns) == 0:
                return

            con = _sqlite.connect(self.meas.database_name)
            cur = con.cursor()

            msg = 'Delete selected database records?'
            reply = _QMessageBox.question(
                self, 'Message', msg, _QMessageBox.Yes, _QMessageBox.No)
            if reply == _QMessageBox.Yes:
                seq = ','.join(['?']*len(idns))
                cur.execute('DELETE FROM {0} WHERE id IN ({1})'.format(
                    table_name, seq), idns)
                con.commit()
                con.close()
                return True
            else:
                con.close()
                return
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            msg = 'Failed to delete database records.'
            _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)
            return

    def getCurrentTableName(self):
        """Get current table name."""
        try:
            current_table = self.getCurrentTable()
            if current_table is not None:
                current_table_name = current_table.table_name
            else:
                current_table_name = None
            return current_table_name
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            return None

    def getCurrentTable(self):
        """Get current table."""
        try:
            idx = self.ui.twg_database.currentIndex()
            if len(self._tables) > idx and idx != -1:
                current_table = self._tables[idx]
                return current_table
            else:
                return None
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            return None

    def getTableSelectedIDs(self, table_name):
        """Get table selected IDs."""
        current_table = self.getCurrentTable()
        if current_table is None:
            return []

        if current_table.table_name != table_name:
            return []

        return current_table.getSelectedIDs()

    def getSelectedIDs(self):
        """Get selected IDs."""
        selected = self.selectedItems()
        rows = [s.row() for s in selected if s.row() != 0]
        rows = _np.unique(rows)

        selected_ids = []
        for row in rows:
            if 'id_0' in self.column_names and 'id_f' in self.column_names:
                idx_id_0 = self.column_names.index('id_0')
                idx_id_f = self.column_names.index('id_f')
                id_0 = int(self.item(row, idx_id_0).text())
                id_f = int(self.item(row, idx_id_f).text())
                for idn in range(id_0, id_f + 1):
                    selected_ids.append(idn)
            elif ('id_0' not in self.column_names
                  and 'id_f' not in self.column_names):
                idn = int(self.item(row, 0).text())
                selected_ids.append(idn)

        return selected_ids

    def updateDatabaseTables(self):
        """Update database tables."""
        if not self.isVisible():
            return

        try:
            self.blockSignals(True)
            _QApplication.setOverrideCursor(_Qt.WaitCursor)

            idx = self.ui.twg_database.currentIndex()
            self.clear()
            self.loadDatabase()
            self.scrollDownTables()
            self.ui.twg_database.setCurrentIndex(idx)

            self.blockSignals(False)
            _QApplication.restoreOverrideCursor()

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            self.blockSignals(False)
            _QApplication.restoreOverrideCursor()
            _QMessageBox.critical(
                self, 'Failure', 'Failed to update database.', _QMessageBox.Ok)

    def scrollDownTables(self):
        """Scroll down all tables."""
        for idx in range(len(self._tables)):
            self.ui.twg_database.setCurrentIndex(idx)
#            self._tables[idx].scrollDown()

    def loadDatabase(self):
        """Load database."""
        try:
            table = DatabaseTable()
            tab = _QWidget()
            vlayout = _QVBoxLayout()
            hlayout = _QHBoxLayout()

            initial_id_la = _QLabel("Initial ID:")
            initial_id_sb = _QSpinBox()
            initial_id_sb.setMinimumWidth(100)
            initial_id_sb.setButtonSymbols(2)
            hlayout.addStretch(0)
            hlayout.addWidget(initial_id_la)
            hlayout.addWidget(initial_id_sb)
            hlayout.addSpacing(30)

            max_number_rows_la = _QLabel("Maximum number of rows:")
            max_number_rows_sb = _QSpinBox()
            max_number_rows_sb.setMinimumWidth(100)
            max_number_rows_sb.setButtonSymbols(2)
            hlayout.addWidget(max_number_rows_la)
            hlayout.addWidget(max_number_rows_sb)
            hlayout.addSpacing(30)

            number_rows_la = _QLabel("Current number of rows:")
            number_rows_sb = _QSpinBox()
            number_rows_sb.setMinimumWidth(100)
            number_rows_sb.setButtonSymbols(2)
            number_rows_sb.setReadOnly(True)
            hlayout.addWidget(number_rows_la)
            hlayout.addWidget(number_rows_sb)

            table_name = self.meas.db_get_collections()
            table.loadDatabaseTable(
                self.meas.database_name,
                table_name,
                initial_id_sb,
                number_rows_sb,
                max_number_rows_sb)

            vlayout.addWidget(table)
            vlayout.addLayout(hlayout)
            tab.setLayout(vlayout)

            self._tables.append(table)
            for name in table_name:
                self.ui.twg_database.addTab(tab, name)

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            msg = 'Failed to load database.'
            _QMessageBox.critical(self, 'Failure', msg, _QMessageBox.Ok)
            return


class DatabaseTable(_QTableWidget):
    """Database table widget."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultSectionSize(120)

        self.database = None
        self.table_name = None
        self.column_names = []
        self.data_types = []
        self.data = []
        self.initial_table_id = None
        self.initial_id_sb = None
        self.number_rows_sb = None
        self.max_number_rows_sb = None
        self.meas = _meas

    def changeInitialID(self):
        """Change initial ID."""
        initial_id = self.initial_id_sb.value()
        self.filterData(initial_id=initial_id)

    def changeMaxRows(self):
        """Change maximum number of rows."""
        self.filterData()

    def loadDatabaseTable(
            self, database, table_name,
            initial_id_sb, number_rows_sb, max_number_rows_sb):
        """Set database filename and table name."""
        self.database = database
        self.table_name = table_name

        self.initial_id_sb = initial_id_sb
        self.initial_id_sb.editingFinished.connect(self.changeInitialID)

        self.max_number_rows_sb = max_number_rows_sb
        self.max_number_rows_sb.setMaximum(_limit_number_rows)
        self.max_number_rows_sb.setValue(_max_number_rows)
        self.max_number_rows_sb.editingFinished.connect(self.changeMaxRows)

        self.number_rows_sb = number_rows_sb
        self.number_rows_sb.setMaximum(_limit_number_rows)
        self.number_rows_sb.setValue(_max_number_rows)

        self.updateTable()

    def updateTable(self):
        """Update table."""
        if self.database is None or self.table_name is None:
            return

        self.blockSignals(True)
        self.setColumnCount(0)
        self.setRowCount(0)

        self.column_names = self.meas.db_get_field_names()
        self.data_types = self.meas.db_get_field_types()
        self.setColumnCount(len(self.column_names))
        self.setHorizontalHeaderLabels(self.column_names)

        self.setRowCount(1)
        for j in range(len(self.column_names)):
            self.setItem(0, j, _QTableWidgetItem(''))
        data = self.meas.db_search_collection(
            self.column_names, filters=None,
            initial_idn=None, max_nr_lines=None)

        if len(data) > 0:
            min_idn = self.meas.db_get_first_id()
            self.initial_id_sb.setMinimum(min_idn)

            max_idn = self.meas.db_get_last_id()
            self.initial_id_sb.setMaximum(max_idn)

            self.max_number_rows_sb.setValue(len(data))
            self.data = data[:]
            self.addRowsToTable(data)
        else:
            self.initial_id_sb.setMinimum(0)
            self.initial_id_sb.setMaximum(0)
            self.max_number_rows_sb.setValue(0)

        self.setSelectionBehavior(_QAbstractItemView.SelectRows)
        self.blockSignals(False)
        self.itemChanged.connect(self.filterChanged)
        self.itemSelectionChanged.connect(self.selectLine)

    def filterChanged(self, item):
        """Apply column filter to data."""
        if item.row() == 0:
            self.filterData()

    def filterData(self, initial_id=None):
        """Apply column filter to data."""
        if (self.rowCount() == 0
           or self.columnCount() == 0
           or len(self.column_names) == 0 or len(self.data_types) == 0):
            return

        max_rows = self.max_number_rows_sb.value()

        filters = []
        for idx in range(len(self.column_names)):
            filters.append(self.item(0, idx).text())

        field_names = self.meas.db_get_field_names()
        self.data = self.meas.db_search_collection(
            field_names, filters, initial_id, max_rows)

        self.addRowsToTable(self.data)

    def addRowsToTable(self, data):
        """Add rows to table."""
        if len(self.column_names) == 0:
            return

        self.setRowCount(1)

        if len(data) > self.max_number_rows_sb.value():
            tabledata = data[-self.max_number_rows_sb.value()::]
        else:
            tabledata = data

        if len(tabledata) == 0:
            return

        self.initial_id_sb.setValue(int(tabledata[0]['id']))
        self.setRowCount(len(tabledata) + 1)
        self.number_rows_sb.setValue(len(tabledata))
        self.initial_table_id = tabledata[0]['id']

        for j in range(len(self.column_names)):
            for i in range(len(tabledata)):
                item_str = str(tabledata[i][self.column_names[j]])
                if len(item_str) > _max_str_size:
                    item_str = item_str[:10] + '...'
                item = _QTableWidgetItem(item_str)
                item.setFlags(_Qt.ItemIsSelectable | _Qt.ItemIsEnabled)
                self.setItem(i + 1, j, item)

    def scrollDown(self):
        """Scroll down."""
        vbar = self.verticalScrollBar()
        vbar.setValue(vbar.maximum())

    def selectLine(self):
        """Select the entire line."""
        if (self.rowCount() == 0
           or self.columnCount() == 0
           or len(self.column_names) == 0 or len(self.data_types) == 0):
            return

        selected = self.selectedItems()
        rows = [s.row() for s in selected]

        if 0 in rows:
            self.setSelectionBehavior(_QAbstractItemView.SelectItems)
        else:
            self.setSelectionBehavior(_QAbstractItemView.SelectRows)

    def getSelectedIDs(self):
        """Get selected IDs."""
        selected = self.selectedItems()
        rows = [s.row() for s in selected if s.row() != 0]
        rows = _np.unique(rows)

        selected_ids = []
        for row in rows:
            if 'id_0' in self.column_names and 'id_f' in self.column_names:
                idx_id_0 = self.column_names.index('id_0')
                idx_id_f = self.column_names.index('id_f')
                id_0 = int(self.item(row, idx_id_0).text())
                id_f = int(self.item(row, idx_id_f).text())
                for idn in range(id_0, id_f + 1):
                    selected_ids.append(idn)
            elif ('id_0' not in self.column_names
                  and 'id_f' not in self.column_names):
                idn = int(self.item(row, 0).text())
                selected_ids.append(idn)

        return selected_ids
