"""Stretched Wire configuration module."""

import numpy as _np
import collections as _collections
from imautils.db.database import DatabaseAndFileDocument


class StretchedWireConfig(DatabaseAndFileDocument):
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

    def __init__(self, database_name=None, mongo=False, server=None):
        """Initialize object.

        Args:
            database_name (str): database file path (sqlite) or name (mongo).
            mongo (bool): flag indicating mongoDB (True) or sqlite (False).
            server (str): MongoDB server.

        """
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
        super().__init__(database_name=database_name,
                         mongo=mongo, server=server)

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


class PowerSupplyConfig(DatabaseAndFileDocument):
    """Read, write and store Power Supply configuration data."""

    label = 'PowerSupply'
    collection_name = 'power_supply'
    db_dict = _collections.OrderedDict([
        ('idn', {'field': 'id', 'dtype': int, 'not_null': True}),
        ('date', {'field': 'date', 'dtype': str, 'not_null': True}),
        ('hour', {'field': 'hour', 'dtype': str, 'not_null': True}),
        ('ps_name', {'field': 'name', 'dtype': str, 'not_null': True}),
        ('ps_type', {'field': 'type', 'dtype': int, 'not_null': True}),
        ('dclink', {'field': 'dclink', 'dtype': float, 'not_null': False}),
        ('ps_setpoint',
            {'field': 'setpoint', 'dtype': float, 'not_null': True}),
        ('maximum_current',
            {'field': 'maximum current', 'dtype': float, 'not_null': True}),
        ('minimum_current',
            {'field': 'minimum current', 'dtype': float, 'not_null': True}),
        ('dcct',
            {'field': 'DCCT Enabled', 'dtype': int, 'not_null': True}),
        ('dcct_head',
            {'field': 'DCCT Head', 'dtype': int, 'not_null': True}),
        ('Kp', {'field': 'Kp', 'dtype': float, 'not_null': True}),
        ('Ki', {'field': 'Ki', 'dtype': float, 'not_null': True}),
        ('current_array', {
            'field': 'current array',
            'dtype': _np.ndarray, 'not_null': False}),
        ('trapezoidal_array', {
            'field': 'trapezoidal array',
            'dtype': _np.ndarray, 'not_null': False}),
        ('trapezoidal_offset', {
            'field': 'trapezoidal offset',
            'dtype': float, 'not_null': True}),
        ('sinusoidal_amplitude', {
            'field': 'sinusoidal amplitude',
            'dtype': float, 'not_null': True}),
        ('sinusoidal_offset', {
            'field': 'sinusoidal offset',
            'dtype': float, 'not_null': True}),
        ('sinusoidal_frequency', {
            'field': 'sinusoidal frequency',
            'dtype': float, 'not_null': True}),
        ('sinusoidal_ncycles', {
            'field': 'sinusoidal cycles',
            'dtype': int, 'not_null': True}),
        ('sinusoidal_phasei', {
            'field': 'sinusoidal initial phase',
            'dtype': float, 'not_null': True}),
        ('sinusoidal_phasef', {
            'field': 'sinusoidal final phase',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_amplitude', {
            'field': 'damped sinusoidal amplitude',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_offset', {
            'field': 'damped sinusoidal offset',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_frequency', {
            'field': 'damped sinusoidal frequency',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_ncycles', {
            'field': 'damped sinusoidal cycles',
            'dtype': int, 'not_null': True}),
        ('dsinusoidal_phasei', {
            'field': 'damped sinusoidal initial phase',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_phasef', {
            'field': 'damped sinusoidal final phase',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal_damp', {
            'field': 'damped sinusoidal damping',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_amplitude', {
            'field': 'damped sinusoidal2 amplitude',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_offset', {
            'field': 'damped sinusoidal2 offset',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_frequency', {
            'field': 'damped sinusoidal2 frequency',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_ncycles', {
            'field': 'damped sinusoidal2 cycles',
            'dtype': int, 'not_null': True}),
        ('dsinusoidal2_phasei', {
            'field': 'damped sinusoidal2 initial phase',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_phasef', {
            'field': 'damped sinusoidal2 final phase',
            'dtype': float, 'not_null': True}),
        ('dsinusoidal2_damp', {
            'field': 'damped sinusoidal2 damping',
            'dtype': float, 'not_null': True}),
    ])

    def __init__(
            self, database_name=None, mongo=False, server=None):
        """Initialize object.

        Args:
            filename (str): connection configuration filepath.
            database_name (str): database file path (sqlite) or name (mongo).
            idn (int): id in database table (sqlite) / collection (mongo).
            mongo (bool): flag indicating mongoDB (True) or sqlite (False).
            server (str): MongoDB server.

        """
        # DC link voltage (90V is the default)
        self.dclink = 90
        # True for DCCT enabled, False for DCCT disabled
        self.dcct = False
        # Power supply status (False = off, True = on)
        self.status = False
        # Power supply loop status (False = open, True = closed)
        self.status_loop = False
        # Power supply connection status (False = no communication)
        self.status_con = False
        # Power supply interlock status (True = active, False = not active)
        self.status_interlock = False
        # Main current
        self.main_current = 0
        # Flag to enable or disable display update
        self.update_display = True

        super().__init__(
            database_name=database_name, mongo=mongo, server=server)

    def get_power_supply_id(self, ps_name):
        """Get power supply database id number."""
        docs = self.db_search_field(self.db_dict['ps_name']['field'], ps_name)

        if len(docs) == 0:
            return None

        return docs[-1][self.db_dict['idn']['field']]

    def get_power_supply_list(self):
        """Get list of power supply names from database."""
        return self.db_get_values(self.db_dict['ps_name']['field'])
