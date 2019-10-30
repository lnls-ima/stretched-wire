# -*- coding: utf-8 -*-
"""Stretched Wire GUI Main Window."""

from qtpy.QtWidgets import (
    QMainWindow as _QMainWindow,
    )
from qtpy.QtGui import QIcon as _QIcon

import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.gui.utils import get_icon_path as _get_icon_path
from stretchedwire.gui.connectionwidget \
 import ConnectionWidget as _ConnectionWidget
from stretchedwire.gui.mainsettingswidget \
 import MainSettingsWidget as _MainSettingsWidget
from stretchedwire.gui.motorandintegratorwidget \
 import MotorandIntegratorWidget as _MotorandIntegratorWidget
from stretchedwire.gui.measurementswidget \
 import MeasurementsWidget as _MeasurementsWidget
from stretchedwire.gui.resultswidget \
 import ResultsWidget as _ResultsWidget


class MainWindow(_QMainWindow):
    """Main Window class for the Stretched Wire GUI."""

    def __init__(self, parent=None, width=500, height=800):
        """Set up the ui and add main tabs."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)
        self.resize(width, height)

        # define tab names and corresponding widgets
        self.tab_names = [
            'Connection',
            'Main Settings',
            'Motor and Integrator',
            'Measurements',
            'Results',
            ]

        self.tab_widgets = [
            _ConnectionWidget(),
            _MainSettingsWidget(),
            _MotorandIntegratorWidget(),
            _MeasurementsWidget(),
            _ResultsWidget(),
            ]

        # add widgets to main tab
        self.ui.twg_main_tab.clear()
        for i in range(len(self.tab_names)):
            tab_name = self.tab_names[i]
            tab = self.tab_widgets[i]
            setattr(self, tab_name, tab)
            icon = _get_icon_path(tab_name)
            self.ui.twg_main_tab.addTab(tab, _QIcon(icon),
                                        tab_name.capitalize())
