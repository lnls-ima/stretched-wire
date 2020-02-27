# -*- coding: utf-8 -*-
"""Connection Widget."""

from qtpy.QtWidgets import QWidget as _QWidget
import qtpy.uic as _uic
import serial.tools.list_ports as _list_ports

from stretchedwire.devices import (
    ppmac as _mdriver,
    fdi as _mint,
    ps as _ps
    )
from stretchedwire.data import config as _config

from stretchedwire.gui.utils import get_ui_file as _get_ui_file


class ConnectionWidget(_QWidget):
    """Connection Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.mdriver = _mdriver
        self.mint = _mint
        self.config = _config

        self.connect_signal_slots()
        self.update_serial_ports()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_connect_FDI2056.clicked.connect(
            self.connect_fdi)
        self.ui.pbt_connect_ppmac.clicked.connect(
            self.connect_ppmac)
        self.ui.pbt_connect_ps.clicked.connect(
            self.connect_ps)
        self.ui.pbt_disconnect_FDI2056.clicked.connect(
            self.disconnect_fdi)
        self.ui.pbt_disconnect_ppmac.clicked.connect(
            self.disconnect_ppmac)
        self.ui.pbt_disconnect_ps.clicked.connect(
            self.disconnect_ps)

    def connect_fdi(self):
        """Connect the FDI2056."""
        if self.mint.connect(self.config.fdi_bench):
            self.ui.signal_FDI_connected.setEnabled(True)
        else:
            self.ui.signal_FDI_connected.setEnabled(False)

    def connect_ppmac(self):
        """Connect the PowerBrick LV."""
        if self.mdriver.connect(self.config.ppmac_ip):
            self.ui.signal_ppmac_connected.setEnabled(True)
        else:
            self.ui.signal_ppmac_connected.setEnabled(False)

    def connect_ps(self):
        _ps.Connect(self.ui.cmb_ps_port.currentText())
        self.ui.signal_ps_connected.setEnabled(_ps.ser.is_open)

    def disconnect_fdi(self):
        """Disconnect the FDI2056."""
        if self.mint.disconnect():
            self.ui.signal_FDI_connected.setEnabled(False)

    def disconnect_ppmac(self):
        """Disconnect the PowerBrick LV."""
        if self.mdriver.disconnect():
            self.ui.signal_ppmac_connected.setEnabled(False)

    def disconnect_ps(self):
        _ps.Disconnect()
        self.ui.signal_ps_connected.setEnabled(_ps.ser.is_open)

    def update_serial_ports(self):
        """Update avaliable serial ports."""
        _l = [p[0] for p in _list_ports.comports()]

        if len(_l) == 0:
            return

        _ports = []
        _s = ''
        _k = str
        if 'COM' in _l[0]:
            _s = 'COM'
            _k = int

        for key in _l:
            _ports.append(key.strip(_s))
        _ports.sort(key=_k)
        _ports = [_s + key for key in _ports]

        self.ui.cmb_ps_port.clear()
        self.ui.cmb_ps_port.addItems(_ports)
