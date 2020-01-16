# -*- coding: utf-8 -*-
"""Motors Widget."""

from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QMessageBox as _QMessageBox,
    )
import qtpy.uic as _uic

import sys as _sys
import traceback as _traceback

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.devices import ppmac as _mdriver
from stretchedwire.data import config as _config


class MotorsWidget(_QWidget):
    """Motors Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.config = _config
        self.mdriver = _mdriver

        # connect signals and slots
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_config_motor.clicked.connect(self.config_motor)
        self.ui.pbt_set_limits.clicked.connect(self.set_limits)
        self.ui.pbt_reset_limits.clicked.connect(self.reset_limits)
        self.ui.pbt_homez.clicked.connect(self.homez)
        self.ui.pbt_home.clicked.connect(self.home)
        self.ui.pbt_kill.clicked.connect(self.kill)
        self.ui.pbt_move_motor.clicked.connect(self.start_motor)
        self.ui.pbt_stop_motor.clicked.connect(self.stop_motor)
        self.ui.pbt_move_axis.clicked.connect(self.start_axis)
        self.ui.pbt_stop_axis.clicked.connect(self.stop_motor)
        self.ui.tbt_home_1.clicked.connect(lambda: self.home_position(1))
        self.ui.tbt_home_2.clicked.connect(lambda: self.home_position(2))
        self.ui.tbt_home_3.clicked.connect(lambda: self.home_position(3))
        self.ui.tbt_home_4.clicked.connect(lambda: self.home_position(4))
        self.ui.tbt_read_1.clicked.connect(lambda: self.read(1))
        self.ui.tbt_read_2.clicked.connect(lambda: self.read(2))
        self.ui.tbt_read_3.clicked.connect(lambda: self.read(3))
        self.ui.tbt_read_4.clicked.connect(lambda: self.read(4))

    def config_motor(self):
        """Configures all motors acceleration and speed."""
        try:
            self.update_config()
            self.mdriver.cfg_motor(1, self.config.m_ac, self.config.m_spdh)
            self.mdriver.cfg_motor(2, self.config.m_ac, self.config.m_spdv)
            self.mdriver.cfg_motor(3, self.config.m_ac, self.config.m_spdh)
            self.mdriver.cfg_motor(4, self.config.m_ac, self.config.m_spdv)
            _QMessageBox.information(self, 'Information',
                                     'Motors configured successfully!',
                                     _QMessageBox.Ok)

        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            _QMessageBox.warning(self, 'Warning',
                                 'Could not configure the motor.\n'
                                 'Please, check the inputs.',
                                 _QMessageBox.Ok)

    def update_config(self):
        self.config.ac = float(self.ui.le_motor_acceleration.text())
        self.config.spdv = float(self.ui.le_motor_vspeed.text())
        self.config.spdh = float(self.ui.le_motor_hspeed.text())
        self.config.motor_calculus()

    def set_limits(self):
        """Set positions limits."""
        try:
            if self.ui.le_limit_min_X.text() == '':
                self.config.limit_min_X = None
            else:
                self.config.limit_min_X = float(self.ui.le_limit_min_X.text())
            if self.ui.le_limit_max_X.text() == '':
                self.config.limit_max_X = None
            else:
                self.config.limit_max_X = float(self.ui.le_limit_max_X.text())
            if self.ui.le_limit_min_Y.text() == '':
                self.config.limit_min_Y = None
            else:
                self.config.limit_min_Y = float(self.ui.le_limit_min_Y.text())
            if self.ui.le_limit_max_Y.text() == '':
                self.config.limit_max_Y = None
            else:
                self.config.limit_max_Y = float(self.ui.le_limit_max_Y.text())
            _QMessageBox.information(self, 'Information',
                                     'Limits configured successfully!',
                                     _QMessageBox.Ok)
        except Exception:
            _traceback.print_exc(file=_sys.stdout)
            _QMessageBox.warning(self, 'Warning',
                                 'Could not configure the limits.\n'
                                 'Please, check the inputs.',
                                 _QMessageBox.Ok)

    def reset_limits(self):
        """Reset positions limits. Set no limits."""
        self.ui.le_limit_min_X.setText('')
        self.ui.le_limit_max_X.setText('')
        self.ui.le_limit_min_Y.setText('')
        self.ui.le_limit_max_Y.setText('')
        self.config.limit_min_X = None
        self.config.limit_max_X = None
        self.config.limit_min_Y = None
        self.config.limit_max_Y = None

    def read(self, motor):
        """Reads all encoders positions and status from ppmac."""
        getattr(self.ui, 'le_encoder_reading_' + str(motor)).setText(
            str(self.mdriver.read_encoder(motor)))
        getattr(self.ui, 'signal_reverse_ls_' + str(motor)).setEnabled(
            int(self.mdriver.get_value(
                'Motor[' + str(motor) + '].MinusLimit')))
        getattr(self.ui, 'signal_forward_ls_' + str(motor)).setEnabled(
            int(self.mdriver.get_value(
                'Motor[' + str(motor) + '].PlusLimit')))
        getattr(self.ui, 'tbt_home_' + str(motor)).setEnabled(
            int(self.mdriver.get_value(
                'Motor[' + str(motor) + '].HomeComplete')))

    def home(self):
        """Home."""
        for m in [1, 2, 3, 4]:
            if getattr(self.ui, 'chb_motor_' + str(m)).isChecked():
                self.mdriver.home(m)

    def homez(self):
        """Zero-move homing."""
        for m in [1, 2, 3, 4]:
            if getattr(self.ui, 'chb_motor_' + str(m)).isChecked():
                self.mdriver.homez(m)

    def kill(self):
        """Kill all motors outputs."""
        for m in [1, 2, 3, 4]:
            if getattr(self.ui, 'chb_motor_' + str(m)).isChecked():
                self.mdriver.kill(m)

    def home_position(self, motor):
        """Jog the motor to the home position."""
        self.mdriver.absolute_move(motor, 0)

    def start_axis(self):
        """Executes an axis jog move."""
        _axis = self.ui.cmb_axis.currentText()
        _pos = float(self.ui.le_axis_dist.text())
        _min_limit = getattr(self.config, 'limit_min_' + _axis)
        _max_limit = getattr(self.config, 'limit_max_' + _axis)
        if ((_min_limit is not None and _pos < _min_limit) or (
                _max_limit is not None and _pos > _max_limit)):
            _QMessageBox.warning(self, 'Warning',
                                 'Position off limits.',
                                 _QMessageBox.Ok)
            return
        self.mdriver.axis_move(_axis, _pos)

    def start_motor(self):
        """Executes a motor jog move."""
        _motor = int(self.ui.cmb_motor.currentText())
        _pos = float(self.ui.le_motor_dist.text())
        if _motor == 1 or _motor == 3:
            _axis = 'X'
        else:
            _axis = 'Y'
        _min_limit = getattr(self.config, 'limit_min_' + _axis)
        _max_limit = getattr(self.config, 'limit_max_' + _axis)
        if ((_min_limit is not None and _pos < _min_limit) or (
                _max_limit is not None and _pos > _max_limit)):
            _QMessageBox.warning(self, 'Warning',
                                 'Position off limits.',
                                 _QMessageBox.Ok)
            return
        self.mdriver.absolute_move(_motor, _pos)

    def stop_motor(self):
        """Stops all motors."""
        self.mdriver.stop_motor(1)
        self.mdriver.stop_motor(2)
        self.mdriver.stop_motor(3)
        self.mdriver.stop_motor(4)
