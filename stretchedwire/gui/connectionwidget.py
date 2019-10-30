# -*- coding: utf-8 -*-
"""Connection Widget."""

from qtpy.QtWidgets import QWidget as _QWidget
import qtpy.uic as _uic

from stretchedwire.devices import ppmac as _mdriver
from stretchedwire.devices import fdi as _mint
from stretchedwire.data import config as _config

from stretchedwire.gui.utils import get_ui_file as _get_ui_file
from stretchedwire.gui.utils import get_icon_path as _get_icon_path


class ConnectionWidget(_QWidget):
    """Connection Widget class."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        _icon = _get_icon_path('ppmac')
        self.ui.la_ppmac.setStyleSheet(
            'border-image: url(' + _icon + ');')

        _icon = _get_icon_path('FDI2056')
        self.ui.la_fdi.setStyleSheet(
            'border-image: url(' + _icon + ');')

        _icon = _get_icon_path('lnls')
        self.ui.la_lnls.setStyleSheet(
            'border-image: url(' + _icon + ');')

        self.mdriver = _mdriver
        self.mint = _mint
        self.config = _config

        # connect signals and slots
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """Create signal and slot connections."""
        self.ui.pbt_connect_FDI2056.clicked.connect(
            self.connect_fdi)
        self.ui.pbt_connect_ppmac.clicked.connect(
            self.connect_ppmac)
        self.ui.pbt_disconnect_FDI2056.clicked.connect(
            self.disconnect_fdi)
        self.ui.pbt_disconnect_ppmac.clicked.connect(
            self.disconnect_ppmac)

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

    def disconnect_fdi(self):
        """Disconnect the FDI2056."""
        if self.mint.disconnect():
            self.ui.signal_FDI_connected.setEnabled(False)
        else:
            self.ui.signal_FDI_connected.setEnabled(True)

    def disconnect_ppmac(self):
        """Disconnect the PowerBrick LV."""
        if self.mdriver.disconnect():
            self.ui.signal_ppmac_connected.setEnabled(False)
        else:
            self.ui.signal_ppmac_connected.setEnabled(True)
