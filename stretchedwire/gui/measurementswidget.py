# -*- coding: utf-8 -*-
"""Measurements Widget."""

import os as _os
import sys as _sys
import time as _time
import numpy as _np
import traceback as _traceback
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QFileDialog as _QFileDialog,
    QApplication as _QApplication,
    QMessageBox as _QMessageBox,
    )
import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.devices import ppmac as _mdriver
from stretchedwire.devices import fdi as _mint
from stretchedwire.data import config as _config
from stretchedwire.data import meas as _meas


class MeasurementsWidget(_QWidget):
    """Measurements Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.mdriver = _mdriver
        self.mint = _mint
        self.config = _config
        self.meas = _meas

        self.list_config_files()
        
        # connect signals and slots
        self.connect_signal_slots()
        
        # temporarily disabling measurement button
        #self.ui.pbt_start_meas.setEnabled(False)

    def closeEvent(self, event):
        """Close widget."""
        try:
            self.mdriver.abort_motion_prog()
            event.accept()
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            event.accept()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_start_meas.clicked.connect(self.start_meas)
        self.ui.pbt_stop_meas.clicked.connect(self.stop_meas)
        self.ui.pbt_save_config.clicked.connect(self.save_config)
        self.ui.cmb_config.currentIndexChanged.connect(self.load)

    def start_meas(self):
        """Starts a new measurement."""
        self.stop = False
        self.update_config()
        self.mint.start_measurement()
        self.config.meas_calculus()
        self.mdriver.run_motion_prog(self.config.type, self.config.axis)

        # start collecting data
        _time0 = _time.time()
        _count = self.mint.get_data_count()
        while ((_count != self.config.n_pts) and (self.stop is False)):
            _count = self.mint.get_data_count()
            if (_time.time() - _time0) > self.config.time_limit:
                _QMessageBox.warning(self, 'Warning', 'Timeout while '
                                     'waiting for integrator data.',
                                     _QMessageBox.Ok)
                return
            _QApplication.processEvents()

        if self.stop is False:
            _results = self.mint.get_data()
            _results = _results.strip('\n').split(',')
            for i in range(len(_results)):
                try:
                    _results[i] = float(_results[i].strip(' WB'))
                except Exception:
                    _traceback.print_exc(file=_sys.stdout)
                    if 'NAN' in _results[i]:
                        _QMessageBox.warning(self, 'Warning',
                                             'Integrator tension over-range.\n'
                                             'Please configure a lower gain.',
                                             _QMessageBox.Ok)
                    return

            self.meas.raw_curve = _np.array(_results, dtype=_np.float64)
            try:
                _tmp = self.meas.raw_curve.reshape(
                    self.config.n_scans,
                    self.config.n_pts).transpose()
            except Exception:
                _traceback.print_exc(file=_sys.stdout)
                return

            self.ui.gv_rawcurves.plotItem.curves.clear()
            self.ui.gv_rawcurves.clear()
            self.ui.gv_rawcurves.plotItem.setLabel(
                'left', "Amplitude", units="V.s")
            self.ui.gv_rawcurves.plotItem.setLabel(
                'bottom', "Points")
            self.ui.gv_rawcurves.plotItem.showGrid(
                x=True, y=True, alpha=0.2)

            px = _np.linspace(0, len(self.meas.raw_curve)-1,
                              len(self.meas.raw_curve))
            self.ui.gv_rawcurves.plotItem.plot(
                px, self.meas.raw_curve, pen=(255, 0, 0), symbol=None)

    def stop_meas(self):
        """Aborts measurement."""
        self.mdriver.abort_motion_prog()
        # _comm.fdi.stop_measurement()
        self.stop = True

    def load(self):
        """Loads configuration set."""
        filename = self.ui.cmb_config.currentText() + '.cfg'
        if filename != '':
            self.config.read_file(filename)

        # self.ui.le_motor_acceleration.setText(str(self.config.ac))
        # self.ui.le_motor_vspeed.setText(str(self.config.spdv))
        # self.ui.le_motor_hspeed.setText(str(self.config.spdh))
        # self.ui.cmb_integrator_gain.setCurrentText(str(self.config.gain))
        # self.ui.cmb_integration_pts.setCurrentText(str(self.config.n_pts))

        self.ui.le_operator.setText(self.config.operator)
        self.ui.le_magnet_name.setText(self.config.magnet_name)
        self.ui.cmb_meas_axis.setCurrentText(self.config.axis)
        self.ui.le_motor_meas_dist.setText(str(self.config.analysis_interval))
        self.ui.cmb_meas_integral.setCurrentText(self.config.type)
        self.ui.te_meas_details.setText(self.config.comments)

    def save_config(self):
        """Save current configuration to file."""
        self.update_config()
        default_filename = self.ui.cmb_config.currentText()
        filename = _QFileDialog.getSaveFileName(
            self, caption='Open configuration file',
            directory=default_filename, filter="Configuration files (*.cfg)")

        if isinstance(filename, tuple):
            filename = filename[0]

        if len(filename) == 0:
            return

        self.config.save_file(filename)
        self.ui.cmb_config.addItem(filename)

    def list_config_files(self):
        """List configuration files and insert in the combobox."""
        file_list = _os.listdir()
        cfg_list = []
        for file in file_list:
            if '.cfg' in file:
                cfg_list.append(file.split('.')[0])

        cfg_list.sort()
        self.ui.cmb_config.addItems(cfg_list)
        self.ui.cmb_config.setCurrentIndex(-1)

    def update_config(self):
        self.config.magnet_name = self.ui.le_magnet_name.text().upper()
        self.config.operator = self.ui.le_operator.text()
        self.config.axis = self.ui.cmb_meas_axis.currentText()
        self.config.analysis_interval = float(
            self.ui.le_motor_meas_dist.text())
        self.config.type = self.ui.cmb_meas_integral.currentText()
        self.config.comments = self.ui.te_meas_details.toPlainText()
