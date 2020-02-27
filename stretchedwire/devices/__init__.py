"""Sub-package for devices communication."""

import os as _os
import numpy as _np
import time as _time
from imautils.devices import PmacLV_IMS
from imautils.devices import FDI2056
from imautils.devices import Agilent34401ALib as _Agilent34401ALib
from imautils.devices import pydrs as _DRSLib
from imautils.devices.utils import configure_logging


_timestamp = _time.strftime('%Y-%m-%d_%H-%M-%S', _time.localtime())

_logs_path = _os.path.join(
    _os.path.dirname(_os.path.dirname(
        _os.path.dirname(
            _os.path.abspath(__file__)))), 'logs')

if not _os.path.isdir(_logs_path):
    _os.mkdir(_logs_path)

logfile = _os.path.join(
    _logs_path, '{0:s}_stretched_wire_control.log'.format(_timestamp))
configure_logging(logfile)


class DCCT(_Agilent34401ALib.Agilent34401AGPIB):
    """DCCT Multimeter."""

    def __init__(self, log=False):
        super().__init__(log=log)
        self.dcct_head = None

    def read_current(self):
        """Read dcct voltage and convert to current."""
        voltage = self.read()
        dcct_heads = [40, 160, 320, 600, 1000, 1125]
        if voltage is not None and self.dcct_head in dcct_heads:
            current = voltage * self.dcct_head/10
        else:
            current = _np.nan
        return current


class PowerSupply(_DRSLib.SerialDRS):
    """Power Supply."""

    def __init__(self):
        self.ps_type = None
        super().__init__()


ppmac = PmacLV_IMS.EthernetCom()
fdi = FDI2056.EthernetCom()
dcct = DCCT(log=True)
ps = PowerSupply()
