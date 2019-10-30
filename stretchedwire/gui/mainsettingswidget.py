# -*- coding: utf-8 -*-
"""Main Settings Widget."""

from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QMessageBox as _QMessageBox,
    )
import qtpy.uic as _uic

import os as _os
import sys as _sys
import traceback as _traceback
import collections as _collections

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.devices import ppmac as _mdriver
from stretchedwire.devices import fdi as _mint
from stretchedwire.data import config as _config


class MainSettingsWidget(_QWidget):
    """Main Settings Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.config = _config
        self.mdriver = _mdriver
        self.mint = _mint

        # connect signals and slots
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_config_motor.clicked.connect(self.config_motor)
        self.ui.pbt_config_integrator.clicked.connect(self.config_integrator)

    def config_motor(self):
        """Configures trigger signal and
        all motors acceleration and speed."""
        try:
            self.update_config()
            self.mdriver.cfg_motor(1, self.config.m_ac, self.config.m_spdh)
            self.mdriver.cfg_motor(2, self.config.m_ac, self.config.m_spdv)
            self.mdriver.cfg_motor(3, self.config.m_ac, self.config.m_spdh)
            self.mdriver.cfg_motor(4, self.config.m_ac, self.config.m_spdv)
            self.mdriver.cfg_trigger_signal(50000)

            _QMessageBox.information(self, 'Information',
                                     'Motors configured successfully!',
                                     _QMessageBox.Ok)

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            _QMessageBox.warning(self, 'Warning',
                                 'Could not configure the motor.\n'
                                 'Please, check the inputs.',
                                 _QMessageBox.Ok)

    def config_integrator(self):
        """Configures the FDI2056."""
        try:
            self.update_config()
            self.mint.config_measurement_ext_trigger(
                self.config.gain, self.config.n_pts)

            _QMessageBox.information(self, 'Information',
                                     'Integrator configured successfully.',
                                     _QMessageBox.Ok)

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            _QMessageBox.warning(self, 'Warning',
                                 'Could not configure the integrator.\n'
                                 'Please, check the inputs.',
                                 _QMessageBox.Ok)

    def update_config(self):
        self.config.ac = float(self.ui.le_motor_acceleration.text())
        self.config.spdv = float(self.ui.le_motor_vspeed.text())
        self.config.spdh = float(self.ui.le_motor_hspeed.text())
        self.config.motor_calculus()

        self.config.gain = int(self.ui.cmb_integrator_gain.currentText())
        self.config.n_pts = int(self.ui.cmb_integration_pts.currentText())
