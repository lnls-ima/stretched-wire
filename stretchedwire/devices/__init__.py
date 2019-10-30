"""Sub-package for devices communication."""

from imautils.devices import PmacLV_IMS
from imautils.devices import FDI2056

ppmac = PmacLV_IMS.EthernetCom()
fdi = FDI2056.EthernetCom()
