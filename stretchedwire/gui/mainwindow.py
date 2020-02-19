# -*- coding: utf-8 -*-
"""Stretched Wire GUI Main Window."""

from qtpy.QtWidgets import (
    QMainWindow as _QMainWindow,
    QFileDialog as _QFileDialog,
    QApplication as _QApplication,
    )
from qtpy.QtGui import QIcon as _QIcon
import sys as _sys
import traceback as _traceback
import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.gui.utils import get_icon_path as _get_icon_path
from stretchedwire.gui.connectionwidget \
 import ConnectionWidget as _ConnectionWidget
from stretchedwire.gui.motorswidget \
 import MotorsWidget as _MotorsWidget
from stretchedwire.gui.integratorwidget \
 import IntegratorWidget as _IntegratorWidget
from stretchedwire.gui.measurementswidget \
 import MeasurementsWidget as _MeasurementsWidget
from stretchedwire.gui.resultswidget \
 import ResultsWidget as _ResultsWidget
from stretchedwire.gui.databasewidget \
 import DatabaseWidget as _DatabaseWidget

from stretchedwire.data import meas as _meas


class MainWindow(_QMainWindow):
    """Main Window class for the Stretched Wire GUI."""

    def __init__(self, parent=None, width=500, height=800):
        """Set up the ui and add main tabs."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)
        self.resize(width, height)

        self.meas = _meas

        # define tab names and corresponding widgets
        self.tab_names = [
            'Connection',
            'Motors',
            'Integrator',
            'Measurements',
            'Results',
            'Database'
            ]

        self.tab_widgets = [
            _ConnectionWidget(),
            _MotorsWidget(),
            _IntegratorWidget(),
            _MeasurementsWidget(),
            _ResultsWidget(),
            _DatabaseWidget(),
            ]

        # show database name
        self.ui.le_database.setText(self.meas.database_name)

        # add widgets to main tab
        self.ui.twg_main_tab.clear()
        for i in range(len(self.tab_names)):
            tab_name = self.tab_names[i]
            tab = self.tab_widgets[i]
            setattr(self, tab_name, tab)
            icon = _get_icon_path(tab_name)
            self.ui.twg_main_tab.addTab(tab, _QIcon(icon),
                                        tab_name.capitalize())

        self.connect_signal_slots()

    def connect_signal_slots(self):
        self.ui.tbt_database.clicked.connect(self.changeDatabase)

    @property
    def database(self):
        """Return the database filename."""
        return _QApplication.instance().database

    @database.setter
    def database(self, value):
        _QApplication.instance().database = value

    @property
    def directory(self):
        """Return the default directory."""
        return _QApplication.instance().directory

    def changeDatabase(self):
        """Change database file."""
        fn = _QFileDialog.getOpenFileName(
            self, caption='Database file', directory=self.directory,
            filter="Database File (*.db)")

        if isinstance(fn, tuple):
            fn = fn[0]

        if len(fn) == 0:
            return

        self.meas.database_name = fn
        self.ui.le_database.setText(self.meas.database_name)

    def closeEvent(self, event):
        """Close main window and tabs."""
        try:
            for tab in self.tab_widgets:
                tab.close()
            event.accept()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            event.accept()
