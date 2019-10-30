"""Stretched Wire measurements module."""

import sys as _sys
import numpy as _np
import traceback as _traceback
import collections as _collections
from imautils.db.configuration import Configuration


class StretchedWireMeas(Configuration):
    """Stretched Wire measurements class."""

    _label = 'Stretched Wire'
    _db_table = 'measurements'
    _db_dict = _collections.OrderedDict([
        ('raw_data', {'column': 'raw_data', 'dtype': _np.ndarray,
                      'not_null': True}),
        ('first_integral', {'column': 'first_integral', 'dtype': _np.ndarray,
                            'not_null': True}),
        ('second_integral', {'column': 'second_integral', 'dtype': _np.ndarray,
                             'not_null': True}),
    ])

    def __init__(self):
        self.raw_data = _np.array([], dtype=_np.float64)
        self.first_integral = _np.array([], dtype=_np.float64)
        self.second_integral = _np.array([], dtype=_np.float64)

    def first_integral_calculus(self):
        pass

    def second_integral_calculus(self):
        pass
