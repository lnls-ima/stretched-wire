"""Stretched Wire measurements module."""

import numpy as _np
import collections as _collections
from imautils.db.database import DatabaseAndFileDocument


class StretchedWireMeas(DatabaseAndFileDocument):
    """Stretched Wire measurements class."""

    mongo = False
    label = 'Stretched Wire Measurement'
    collection_name = 'measurements'
    db_dict = _collections.OrderedDict([
        ('idn', {'field': 'id', 'dtype': int, 'not_null': True}),
        ('date', {'field': 'date', 'dtype': str, 'not_null': True}),
        ('hour', {'field': 'hour', 'dtype': str, 'not_null': True}),
        ('operator', {'field': 'operator', 'dtype': str,
                      'not_null': False}),
        ('magnet_name', {'field': 'magnet name', 'dtype': str,
                         'not_null': False}),
        ('axis1', {'field': 'measurement axis1', 'dtype': str,
                   'not_null': False}),
        ('type', {'field': 'measurement type', 'dtype': str,
                  'not_null': False}),
        ('comments', {'field': 'comments', 'dtype': str,
                      'not_null': False}),
        ('start', {'field': 'start', 'dtype': float,
                   'not_null': False}),
        ('end', {'field': 'end', 'dtype': float,
                 'not_null': False}),
        ('step', {'field': 'step', 'dtype': float,
                  'not_null': False}),
        ('extra', {'field': 'extra', 'dtype': float,
                   'not_null': False}),
        ('vel', {'field': 'vel', 'dtype': float,
                 'not_null': False}),
        ('raw_data', {'field': 'raw data', 'dtype': _np.ndarray,
                      'not_null': True}),
        ('first_integral', {'field': 'first integral', 'dtype': _np.ndarray,
                            'not_null': True}),
        ('second_integral', {'field': 'second integral', 'dtype': _np.ndarray,
                             'not_null': True}),
    ])

    def __init__(
            self, database_name=None, mongo=False, server=None):
        """Initialize object.

        Args:
            database_name (str): database file path (sqlite) or name (mongo).
            mongo (bool): flag indicating mongoDB (True) or sqlite (False).
            server (str): MongoDB server.

        """
        self.operator = ''
        self.magnet_name = ''
        self.axis1 = ''
        self.type = ''
        self.comments = ''
        self.start = None
        self.end = None
        self.step = None
        self.extra = None
        self.vel = None
        self.raw_data = None
        self.first_integral = _np.ndarray([])
        self.second_integral = _np.ndarray([])
        super().__init__(database_name=database_name,
                         mongo=mongo, server=server)

    def first_integral_calculus(self):
        pass

    def second_integral_calculus(self):
        pass
