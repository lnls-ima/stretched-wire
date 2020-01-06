"""Stretched Wire configuration module."""

import sys as _sys
import numpy as _np
import traceback as _traceback
import collections as _collections
from imautils.db.configuration import Configuration


class StretchedWireConfig(Configuration):
    """Stretched Wire configuration parameters class."""

    label = 'Stretched Wire Configuration'
    collection_name = 'configuration'
    db_dict = _collections.OrderedDict([
        ('idn', {'field': 'id', 'dtype': int, 'not_null': True}),
        ('date', {'field': 'date', 'dtype': str, 'not_null': True}),
        ('hour', {'field': 'hour', 'dtype': str, 'not_null': True}),
        ('operator', {'field': 'operator', 'dtype': str,
                      'not_null': True}),
        ('magnet_name', {'field': 'magnet_name', 'dtype': str,
                         'not_null': True}),
        ('axis', {'field': 'measurement_axis', 'dtype': str,
                  'not_null': True}),
        ('type', {'field': 'measurement_type', 'dtype': str,
                  'not_null': True}),
        ('comments', {'field': 'comments', 'dtype': str,
                      'not_null': False}),
        ('initial_pos', {'field': 'initial_pos', 'dtype': float,
                               'not_null': True}),
        ('final_pos', {'field': 'final_pos', 'dtype': float,
                               'not_null': True}),
        ('pts_dist', {'field': 'pts_dist', 'dtype': float,
                               'not_null': True}),
        ('analysis_interval', {'field': 'analysis_interval', 'dtype': float,
                               'not_null': True}),
        ('n_pts', {'field': 'integration_points', 'dtype': int,
                             'not_null': True}),
        ('gain', {'field': 'integrator_gain', 'dtype': int, 'not_null': True}),
        ('trig_source', {'field': 'trig_source', 'dtype': str,
                         'not_null': True}),
        ('n_scans', {'field': 'n_scans', 'dtype': int, 'not_null': True}),
        ('ac', {'field': 'acceleration', 'dtype': float, 'not_null': True}),
        ('spdv', {'field': 'vertical_speed', 'dtype': float, 
                  'not_null': True}),
        ('spdh', {'field': 'horizontal_speed', 'dtype': float, 
                  'not_null': True}),
    ])

    def __init__(self):
        self.idn = None
        self.date = None
        self.hour = None
        self.ppmac_ip = '10.0.28.51'
        self.fdi_bench = 3
        self.gain = 100
        self.n_pts = 0
        self.trig_source = 'External'
        self.ac = 0.5  # s
        self.spdv = 0.02  # mm/s
        self.spdh = 2  # mm/s
        self.operator = ''
        self.magnet_name = ''
        self.axis = ''
        self.type = ''
        self.comments = ''
        self.initial_pos = 0
        self.final_pos = 0
        self.pts_dist = 0
        self.analysis_interval = 0
        self.n_scans = 1 
        super().__init__()

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
