# -*- coding: utf-8 -*-
"""Results Widget."""

import sys as _sys
import numpy as _np
import traceback as _traceback
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QMessageBox as _QMessageBox,
    )
import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.data import measurement as _meas


class ResultsWidget(_QWidget):
    """Results Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.meas = _meas
        # connect signals and slots
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_save_results.clicked.connect(self.save_results)
        self.ui.pbt_plot_results.clicked.connect(self.plot_results)

    def save_results(self):
        """Saves measurements to file."""
        self.meas.save_file('measurements.dat')

    def plot_results(self):
        """Plots first and second integrals."""
        try:
            self.ui.gv_first_integral.plotItem.curves.clear()
            self.ui.gv_first_integral.clear()
            self.ui.gv_first_integral.plotItem.setLabel(
                'left', "First Integral", units="T.m^2")
            self.ui.gv_first_integral.plotItem.setLabel(
                'bottom', "Points")
            self.ui.gv_first_integral.plotItem.showGrid(
                x=True, y=True, alpha=0.2)

            px = _np.linspace(0, len(self.meas.first_integral)-1,
                              len(self.meas.first_integral))
            self.ui.gv_first_integral.plotItem.plot(
                px, self.meas.first_integral, pen=(255, 0, 0), symbol=None)
        except Exception:
            _QMessageBox.warning(self, 'Warning',
                                 'Could not plot first integral field.\n'
                                 'Please, check your data.',
                                 _QMessageBox.Ok)

        try:
            self.ui.gv_second_integral.plotItem.curves.clear()
            self.ui.gv_second_integral.clear()
            self.ui.gv_second_integral.plotItem.setLabel(
                'left', "Second Integral", units="T.m")
            self.ui.gv_second_integral.plotItem.setLabel(
                'bottom', "Points")
            self.ui.gv_second_integral.plotItem.showGrid(
                x=True, y=True, alpha=0.2)

            px = _np.linspace(0, len(self.meas.second_integral)-1,
                              len(self.meas.second_integral))
            self.ui.gv_second_integral.plotItem.plot(
                px, self.meas.second_integral, pen=(255, 0, 0), symbol=None)
        except Exception:
            _QMessageBox.warning(self, 'Warning',
                                 'Could not plot second integral field.\n'
                                 'Please, check your data.',
                                 _QMessageBox.Ok)
