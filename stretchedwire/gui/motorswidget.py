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
        self.ui.pbt_encoder_reading.clicked.connect(self.read_encoder)
        self.ui.pbt_home.clicked.connect(self.home)
        self.ui.pbt_move_motor.clicked.connect(self.start_motor)
        self.ui.pbt_stop_motor.clicked.connect(self.stop_motor)
        self.ui.pbt_move_axis.clicked.connect(self.start_axis)
        self.ui.pbt_stop_axis.clicked.connect(self.stop_motor)
        self.ui.tbt_home_1.clicked.connect(lambda: self.home_position(1))
        self.ui.tbt_home_2.clicked.connect(lambda: self.home_position(2))
        self.ui.tbt_home_3.clicked.connect(lambda: self.home_position(3))
        self.ui.tbt_home_4.clicked.connect(lambda: self.home_position(4))

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

    def read_encoder(self):
        """Reads all encoders positions and status from ppmac."""
        self.ui.le_encoder_reading_1.setText(
            str(self.mdriver.read_encoder(1)))
        self.ui.le_encoder_reading_2.setText(
            str(self.mdriver.read_encoder(2)))
        self.ui.le_encoder_reading_3.setText(
            str(self.mdriver.read_encoder(3)))
        self.ui.le_encoder_reading_4.setText(
            str(self.mdriver.read_encoder(4)))

        self.ui.signal_reverse_ls_1.setEnabled(
            int(self.mdriver.get_value('Motor[1].MinusLimit')))
        self.ui.signal_forward_ls_1.setEnabled(
            int(self.mdriver.get_value('Motor[1].PlusLimit')))
        self.ui.signal_reverse_ls_2.setEnabled(
            int(self.mdriver.get_value('Motor[2].MinusLimit')))
        self.ui.signal_forward_ls_2.setEnabled(
            int(self.mdriver.get_value('Motor[2].PlusLimit')))
        self.ui.signal_reverse_ls_3.setEnabled(
            int(self.mdriver.get_value('Motor[3].MinusLimit')))
        self.ui.signal_forward_ls_3.setEnabled(
            int(self.mdriver.get_value('Motor[3].PlusLimit')))
        self.ui.signal_reverse_ls_4.setEnabled(
            int(self.mdriver.get_value('Motor[4].MinusLimit')))
        self.ui.signal_forward_ls_4.setEnabled(
            int(self.mdriver.get_value('Motor[4].PlusLimit')))

        self.ui.tbt_home_1.setEnabled(
            int(self.mdriver.get_value('Motor[1].HomeComplete')))
        self.ui.tbt_home_2.setEnabled(
            int(self.mdriver.get_value('Motor[2].HomeComplete')))
        self.ui.tbt_home_3.setEnabled(
            int(self.mdriver.get_value('Motor[3].HomeComplete')))
        self.ui.tbt_home_4.setEnabled(
            int(self.mdriver.get_value('Motor[4].HomeComplete')))

    def home(self):
        """Home all motors."""
        self.mdriver.home(1)
        self.mdriver.home(2)
        self.mdriver.home(3)
        self.mdriver.home(4)
        self.read_encoder()

    def home_position(self, motor):
        """Jog the motor to the home position."""
        self.mdriver.absolute_move(motor, 0)

    def start_axis(self):
        """Executes an axis jog move."""
        _axis = self.ui.cmb_axis.currentText()
        _dist = float(self.ui.le_axis_dist.text())
        self.mdriver.axis_move(_axis, _dist)

    def start_motor(self):
        """Executes a motor jog move."""
        _motor = int(self.ui.cmb_motor.currentText())
        _dist = float(self.ui.le_motor_dist.text())
        self.mdriver.relative_move(_motor, _dist)

    def stop_motor(self):
        """Stops all motors."""
        self.mdriver.stop_motor(1)
        self.mdriver.stop_motor(2)
        self.mdriver.stop_motor(3)
        self.mdriver.stop_motor(4)
