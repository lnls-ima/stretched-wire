"""Stretched Wire configuration module."""

import collections as _collections
from imautils.db.database import DatabaseAndFileDocument


class StretchedWireConfig(DatabaseAndFileDocument):
    """Stretched Wire configuration parameters class."""

    mongo = False
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
        ('axis1', {'field': 'measurement_axis1', 'dtype': str,
                   'not_null': True}),
        ('type', {'field': 'measurement_type', 'dtype': str,
                  'not_null': True}),
        ('comments', {'field': 'comments', 'dtype': str,
                      'not_null': False}),
        ('start', {'field': 'start', 'dtype': float,
                   'not_null': True}),
        ('end', {'field': 'end', 'dtype': float,
                 'not_null': True}),
        ('step', {'field': 'step', 'dtype': float,
                  'not_null': True}),
        ('extra', {'field': 'extra', 'dtype': float,
                   'not_null': True}),
        ('vel', {'field': 'vel', 'dtype': float,
                 'not_null': True}),
        ('analysis_interval', {'field': 'analysis_interval', 'dtype': float,
                               'not_null': True}),
        ('n_pts', {'field': 'integration_points', 'dtype': int,
                   'not_null': True}),
        ('gain', {'field': 'integrator_gain', 'dtype': int, 'not_null': True}),
        ('trig_source', {'field': 'trig_source', 'dtype': str,
                         'not_null': True}),
        ('meas_unit', {'field': 'meas_unit', 'dtype': str, 'not_null': True}),
        ('n_scans', {'field': 'n_scans', 'dtype': int, 'not_null': True}),
        ('ac', {'field': 'acceleration', 'dtype': float, 'not_null': True}),
        ('spdv', {'field': 'vertical_speed', 'dtype': float,
                  'not_null': True}),
        ('spdh', {'field': 'horizontal_speed', 'dtype': float,
                  'not_null': True}),
        ('limit_min_X', {'field': 'limit_min_X', 'dtype': float,
                         'not_null': False}),
        ('limit_max_X', {'field': 'limit_max_X', 'dtype': float,
                         'not_null': False}),
        ('limit_min_Y', {'field': 'limit_min_Y', 'dtype': float,
                         'not_null': False}),
        ('limit_max_Y', {'field': 'limit_max_Y', 'dtype': float,
                         'not_null': False}),
    ])

    def __init__(self):
        self.idn = None
        self.date = None
        self.hour = None
        self.ppmac_ip = '10.0.28.39'
        self.position = 0
        self.fdi_bench = 3
        self.gain = 100
        self.n_pts = 0
        self.trig_source = 'External'
        self.meas_unit = 'V.s'
        self.ac = 0.5  # s
        self.spdv = 0.02  # mm/s
        self.spdh = 2  # mm/s
        self.operator = ''
        self.magnet_name = ''
        self.axis1 = ''
        self.axis2 = ''
        self.type = ''
        self.comments = ''
        self.start = 0
        self.end = 0
        self.step = 0
        self.extra = 0
        self.vel = 0
        self.analysis_interval = 0
        self.n_scans = 1
        self.limit_min_X = None
        self.limit_max_X = None
        self.limit_min_Y = None
        self.limit_max_Y = None
        super().__init__()

    def motor_calculus(self):
        _counts_per_mm = 50000
        self.m_ac = self.ac * 1000  # ms
        self.m_spdv = self.spdv * _counts_per_mm * 0.001  # counts/ms
        self.m_spdh = self.spdh * _counts_per_mm * 0.001  # counts/ms
        self.m_hvel = self.vel * _counts_per_mm * 0.001  # counts/ms
        self.m_vvel = self.vel * _counts_per_mm * 0.001  # counts/ms

    def meas_calculus(self):
        if self.axis1 == 'X':
            _spd = self.spdh
        else:
            _spd = self.spdv

        self.time_limit = (2 * abs(self.analysis_interval/_spd)) + 2
