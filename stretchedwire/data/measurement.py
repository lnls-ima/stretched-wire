"""Stretched Wire measurements module."""

import numpy as _np
import collections as _collections
from imautils.db.configuration import Configuration


class StretchedWireMeas(Configuration):
    """Stretched Wire measurements class."""

    label = 'Stretched Wire Measurement'
    collection_name = 'measurements'
    db_dict = _collections.OrderedDict([
        ('idn', {'field': 'id', 'dtype': int, 'not_null': True}),
        ('date', {'field': 'date', 'dtype': str, 'not_null': True}),
        ('hour', {'field': 'hour', 'dtype': str, 'not_null': True}),
        ('raw_data', {'field': 'raw_data', 'dtype': _np.ndarray,
                      'not_null': True}),
        ('first_integral', {'field': 'first_integral', 'dtype': _np.ndarray,
                            'not_null': True}),
        ('second_integral', {'field': 'second_integral', 'dtype': _np.ndarray,
                             'not_null': True}),
    ])

    def __init__(self):
        self.idn = None
        self.date = None
        self.hour = None
        self.raw_data = _np.array([], dtype=_np.float64)
        self.first_integral = _np.array([], dtype=_np.float64)
        self.second_integral = _np.array([], dtype=_np.float64)
        super().__init__()

    def first_integral_calculus(self):
        pass

    def second_integral_calculus(self):
        pass
