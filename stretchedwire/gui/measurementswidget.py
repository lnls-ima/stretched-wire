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
        self.ui.tbt_save_file.clicked.connect(self.save_measurement)
        self.ui.tbt_save_to_database.clicked.connect(self.save_to_database)

    def start_meas(self):
        """Starts a new measurement."""
        self.stop = False
        self.update_config()
        self.config.meas_calculus()
        _min = getattr(self.config, 'limit_min_' + self.config.axis1)
        _max = getattr(self.config, 'limit_max_' + self.config.axis1)
        print(_max)
        print(self.config.end)
        if self.config.analysis_interval > 0:
            if ((_min is not None and self.config.start < _min) or
                    (_max is not None and self.config.end > _max)):
                _QMessageBox.warning(self, 'Warning',
                                     'Position off the limits.',
                                     _QMessageBox.Ok)
                return
        else:
            if ((_max is not None and self.config.start > _max) or
                    (_min is not None and self.config.end < _min)):
                _QMessageBox.warning(self, 'Warning',
                                     'Position off the limits.',
                                     _QMessageBox.Ok)
                return
        self.mdriver.cfg_measurement_type(self.config.type)
        self.mdriver.cfg_trigger_signal(self.config.start,
                                        self.config.step)

        if self.config.analysis_interval > 0:
            self.mdriver.cfg_measurement(self.config.end + self.config.extra,
                                         self.config.m_ac, self.config.n_scans)
            self.mdriver.axis_move(self.config.axis1,
                                   (self.config.start - self.config.extra))
        else:
            self.mdriver.cfg_measurement(self.config.end - self.config.extra,
                                         self.config.m_ac, self.config.n_scans)
            self.mdriver.axis_move(self.config.axis1,
                                   (self.config.start + self.config.extra))

        _time.sleep(0.5)
        if self.config.axis1 == 'X':
            while(not(self.mdriver.in_position(1))):
                pass
        else:
            while(not(self.mdriver.in_position(2))):
                pass

        self.ui.gv_rawcurves.plotItem.curves.clear()
        self.ui.gv_rawcurves.clear()
        self.ui.gv_rawcurves.plotItem.setLabel(
            'left', "Amplitude", units="V.s")
        self.ui.gv_rawcurves.plotItem.setLabel(
            'bottom', "Position", units='mm')
        self.ui.gv_rawcurves.plotItem.showGrid(
            x=True, y=True, alpha=0.2)

        self.mint.config_trig_external(self.config.n_pts)
        self.mint.start_measurement()
        self.mdriver.run_motion_prog(self.config.type, self.config.axis1)

        # start collecting data
        _time0 = _time.time()
        _count = self.mint.get_data_count()
        while ((_count != self.config.n_pts-1) and (self.stop is False)):
            _count = self.mint.get_data_count()
            '''self.ui.lcd_pos.display(
                self.mdriver.get_position(self.config.axis1))'''
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

            self.meas.raw_data = _np.array(_results, dtype=_np.float64)
            try:
                _tmp = self.meas.raw_data.reshape(
                    self.config.n_scans,
                    self.config.n_pts-1).transpose()
            except Exception:
                _traceback.print_exc(file=_sys.stdout)
                return

            px = _np.linspace(self.config.start, self.config.end,
                              self.config.n_pts-1)
            self.ui.gv_rawcurves.plotItem.plot(
                px, self.meas.raw_data, pen=(0, 0, 0), width=3, symbol=None)
#            self.meas.first_integral_calculus()

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

        self.ui.le_operator.setText(self.config.operator)
        self.ui.le_magnet_name.setText(self.config.magnet_name)
        self.ui.cmb_meas_integral.setCurrentText(self.config.type)
        self.ui.le_comments.setText(self.config.comments)
        getattr(self.ui, 'rb_axis1_'
                + self.config.axis1).setChecked(True)
        getattr(self.ui, 'le_start_'
                + self.config.axis1).setText(str(self.config.start))
        getattr(self.ui, 'le_end_'
                + self.config.axis1).setText(str(self.config.end))
        getattr(self.ui, 'le_step_'
                + self.config.axis1).setText(str(self.config.step))
        getattr(self.ui, 'le_extra_'
                + self.config.axis1).setText(str(self.config.extra))
        getattr(self.ui, 'le_vel_'
                + self.config.axis1).setText(str(self.config.vel))

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
        self.config.type = self.ui.cmb_meas_integral.currentText()
        self.config.comments = self.ui.le_comments.text()
        self.config.n_scans = self.ui.sb_nr_of_measurements.value()
        if self.ui.rb_axis1_X.isChecked():
            self.config.axis1 = 'X'
        elif self.ui.rb_axis1_Y.isChecked():
            self.config.axis1 = 'Y'
        else:
            _QMessageBox.warning(self, 'Warning', 'Please, select an axis.',
                                 _QMessageBox.Ok)
        self.config.start = float(getattr(self.ui, 'le_start_'
                                          + self.config.axis1).text())
        self.config.end = float(getattr(self.ui, 'le_end_'
                                        + self.config.axis1).text())
        self.config.step = float(getattr(self.ui, 'le_step_'
                                         + self.config.axis1).text())
        self.config.extra = float(getattr(self.ui, 'le_extra_'
                                          + self.config.axis1).text())
        self.config.vel = float(getattr(self.ui, 'le_vel_'
                                        + self.config.axis1).text())
        self.config.analysis_interval = (self.config.end
                                         - self.config.start)
        self.config.n_pts = abs(int(self.config.analysis_interval
                                / self.config.step))

    def save_measurement(self):
        """Save current measurement to file."""
        self.update_meas()
        filename = _QFileDialog.getSaveFileName(
            self, caption='Open measurement file',
            directory=self.meas.database_name,
            filter="Text files (*.txt *.dat)")

        if isinstance(filename, tuple):
            filename = filename[0]

        if len(filename) == 0:
            return

        self.meas.save_file(filename)
        self.ui.cmb_config.addItem(filename)

    def save_to_database(self):
        self.update_meas()
        if not self.meas.save_to_database():
            raise Exception("Failed to save database.")

    def update_meas(self):
        self.meas.operator = self.config.operator
        self.meas.magnet_name = self.config.magnet_name
        self.meas.axis1 = self.config.axis1
        self.meas.type = self.config.type
        self.meas.comments = self.config.comments
        self.meas.start = self.config.start
        self.meas.end = self.config.end
        self.meas.step = self.config.step
        self.meas.extra = self.config.extra
        self.meas.vel = self.config.vel
#        self.meas.raw_data = None
#        self.meas.first_integral = None
#        self.meas.second_integral = None
