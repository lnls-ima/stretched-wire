"""Stretched Wire configuration module."""

import sys as _sys
import numpy as _np
import traceback as _traceback
import collections as _collections
from imautils.db.configuration import Configuration


class StretchedWireConfig(Configuration):
    """Stretched Wire configuration parameters class."""

    _label = 'Stretched Wire'
    _db_table = 'configuration'
    _db_dict = _collections.OrderedDict([
        ('operator', {'column': 'operator', 'dtype': str,
                      'not_null': True}),
        ('magnet_name', {'column': 'magnet_name', 'dtype': str,
                         'not_null': True}),
        ('axis', {'column': 'measurement_axis', 'dtype': str,
                  'not_null': True}),
        ('type', {'column': 'measurement_type', 'dtype': str,
                  'not_null': True}),
        ('comments', {'column': 'comments', 'dtype': str,
                      'not_null': True}),
        ('analysis_interval', {'column': 'analysis_interval', 'dtype': float,
                               'not_null': True}),
        ('n_pts', {'column': 'integration_points', 'dtype': int,
                             'not_null': True}),
        ('gain', {'column': 'integrator_gain', 'dtype': int,
                  'not_null': True}),
        ('n_scans', {'column': 'n_scans', 'dtype': int,
                     'not_null': True}),
        ('ac', {'column': 'acceleration', 'dtype': float,
                'not_null': True}),
        ('spdv', {'column': 'vertical_speed', 'dtype': float,
                  'not_null': True}),
        ('spdh', {'column': 'horizontal_speed', 'dtype': float,
                  'not_null': True}),
    ])

    def __init__(self):
        self.ppmac_ip = '10.0.28.51'
        self.fdi_bench = 3
        self.gain = 100
        self.n_pts = 0
        self.ac = 0.5  # s
        self.spdv = 0.02  # mm/s
        self.spdh = 2  # mm/s
        self.operator = ''
        self.magnet_name = ''
        self.axis = ''
        self.type = ''
        self.comments = ''
        self.analysis_interval = 0
        self.n_scans = 1

    def motor_calculus(self):
        _counts_per_mm = 50000
        self.m_ac = self.ac * 1000  # ms
        self.m_spdv = self.spdv * _counts_per_mm * 0.001  # counts/ms
        self.m_spdh = self.spdh * _counts_per_mm * 0.001  # counts/ms

    def meas_calculus(self):
        if self.axis == 'X':
            _spd = self.spdh
        else:
            _spd = self.spdv

        self.time_limit = 2 * self.analysis_interval/_spd
