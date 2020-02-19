# -*- coding: utf-8 -*-
"""Integrator Widget."""

from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QApplication as _QApplication,
    QMessageBox as _QMessageBox,
    QFileDialog as _QFileDialog,
    )
import sys as _sys
import time as _time
import numpy as _np
import traceback as _traceback
import qtpy.uic as _uic

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.devices import fdi as _mint
from stretchedwire.data import config as _config
from stretchedwire.data import meas as _meas


class IntegratorWidget(_QWidget):
    """Integrator Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.mint = _mint
        self.config = _config
        self.meas = _meas

        # connect signals and slots
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_config_integrator.clicked.connect(self.config_integrator)
        self.ui.pbt_meas_timer.clicked.connect(self.measure)
        self.ui.pbt_stop.clicked.connect(self.stop)
        self.ui.pbt_status_update.clicked.connect(self.status_update)
        self.ui.pbt_shut_down.clicked.connect(self.shut_down)
        self.ui.tbt_save_file.clicked.connect(self.save_file)

    def config_integrator(self):
        """Configures the FDI2056."""
        try:
            self.ui.gv_rawcurves_tim.plotItem.curves.clear()
            self.ui.gv_rawcurves_tim.clear()
            self.update_config()
            self.mint.main_settings(self.config.gain, self.config.trig_source)
            if self.config.meas_unit == 'V.s':
                self.mint.send('SENS:FUNC FLUX')
            else:
                self.mint.send('SENS:FUNC VOLT')
            _QMessageBox.information(self, 'Information',
                                     'Integrator configured successfully.',
                                     _QMessageBox.Ok)

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            _QMessageBox.warning(self, 'Warning',
                                 'Could not configure the integrator.\n'
                                 'Please, check the inputs.',
                                 _QMessageBox.Ok)

    def measure(self):
        """Do a zero movement measurement with timer source trigger."""
        _total_time = float(self.ui.le_meas_time.text())
        _rate = float(self.ui.le_timer_rate.text())
        _pts = round(_total_time / (1/_rate))
        _time_limit = 50 * _total_time

        self.mint.config_trig_timer(_rate, _pts)
        self.mint.start_measurement()
        self.stop = False

        self.ui.gv_rawcurves_tim.plotItem.curves.clear()
        self.ui.gv_rawcurves_tim.clear()
        self.ui.gv_rawcurves_tim.plotItem.setLabel(
            'left', "Amplitude", units=self.config.meas_unit)
        self.ui.gv_rawcurves_tim.plotItem.setLabel(
            'bottom', "Points")
        self.ui.gv_rawcurves_tim.plotItem.showGrid(
            x=True, y=True, alpha=0.2)

        # start collecting data
        _time0 = _time.time()
        _count = self.mint.get_data_count()
        while ((_count != _pts-1) and (self.stop is False)):
            _count = self.mint.get_data_count()
            if (_time.time() - _time0) > _time_limit:
                _QMessageBox.warning(self, 'Warning', 'Timeout while '
                                     'waiting for integrator data.',
                                     _QMessageBox.Ok)
                return
            _QApplication.processEvents()

        if self.stop is False:
            _results = self.mint.get_data()
            print(_results)
            _results = _results.strip('\n').split(',')
            for i in range(len(_results)):
                try:
                    if self.config.meas_unit == 'V.s':
                        _results[i] = float(_results[i].strip(' WB'))
                    else:
                        _results[i] = float(_results[i].strip(' V'))
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
                    _pts-1).transpose()
            except Exception:
                _traceback.print_exc(file=_sys.stdout)
                return

            px = _np.linspace(0, len(self.meas.raw_data)-1,
                              len(self.meas.raw_data))
            self.ui.gv_rawcurves_tim.plotItem.plot(
                px, self.meas.raw_data, pen=(255, 0, 0), symbol=None)

#            fft = _np.fft.fft(self.meas.raw_data)
#            freq = _np.fft.fftfreq(self.meas.raw_data.size, 0.0005)
#            plt.plot(freq, fft.real)
#            plt.show()

    def stop(self):
        self.stop = True

    def save_file(self):
        filename = _QFileDialog.getSaveFileName(
            self, caption='Open measurement file',
            directory='Integrator_Measurement',
            filter="Text files (*.txt *.dat)")

        if isinstance(filename, tuple):
            filename = filename[0]

        if len(filename) == 0:
            return

        self.meas.save_file(filename)

    def status_update(self):
        """Updates integrator status on UI."""
        try:
            self.ui.la_status_1.setText(self.mint.status(0))
            self.ui.la_status_2.setText(self.mint.status(1))
            self.ui.la_status_3.setText(self.mint.status(2))
            self.ui.la_status_4.setText(self.mint.status(3))
        except Exception:
            pass

    def shut_down(self):
        """Properly shuts the system down."""
        self.mint.shut_down()

    def update_config(self):
        self.config.gain = int(self.ui.cmb_integrator_gain.currentText())
        self.config.trig_source = self.ui.cmb_trigger_source.currentText()
        if self.ui.cmb_meas_unit.currentText() == 'Flux (V.s)':
            self.config.meas_unit = 'V.s'
        else:
            self.config.meas_unit = 'V'
        if self.config.trig_source == "Timer":
            self.ui.gb_timer.setEnabled(True)
        else:
            self.ui.gb_timer.setEnabled(False)
