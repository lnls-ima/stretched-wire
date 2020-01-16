"""Stretched Wire measurements module."""

import json as _json
import numpy as _np
import collections as _collections
from imautils.db import utils as _utils
from imautils.db.database import DatabaseDocument


_empty_str = '--'


class MeasurementError(Exception):
    """Measurement exception."""

    def __init__(self, message):
        """Initialize object."""
        self.message = message


class Measurement(DatabaseDocument):
    """Base class for measurements."""

    label = ''
    collection_name = ''
    db_dict = {}

    def __init__(
            self, filename=None, database_name=None, idn=None,
            mongo=False, server='localhost'):
        """Initialize object.

        Args:
            filename (str): connection measurement filepath.
            database_name (str): database file path (sqlite) or name (mongo).
            idn (int): id in database table (sqlite) / collection (mongo).
            mongo (bool): flag indicating mongoDB (True) or sqlite (False).
            server (str): MongoDB server.

        """
        super().__init__(
            database_name=database_name, mongo=mongo, server=server)

        if filename is not None and idn is not None:
            raise ValueError('Invalid arguments for Measurement object.')

        if idn is not None and database_name is not None:
            self.read_from_database()

        elif filename is not None:
            self.read_file(filename)

    def __eq__(self, other):
        """Equality method."""
        if isinstance(other, self.__class__):
            if len(self.__dict__) != len(other.__dict__):
                return False

            for key in self.__dict__:
                if key not in other.__dict__:
                    return False

                self_value = self.__dict__[key]
                other_value = other.__dict__[key]

                if callable(self_value):
                    pass
                elif (isinstance(self_value, _np.ndarray) and
                      isinstance(other_value, _np.ndarray)):
                    if not self_value.tolist() == other_value.tolist():
                        return False
                elif (not isinstance(self_value, _np.ndarray) and
                      not isinstance(other_value, _np.ndarray)):
                    if not self_value == other_value:
                        return False
                else:
                    return False

            return True

        else:
            return False

    def __ne__(self, other):
        """Non-equality method."""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __setattr__(self, name, value):
        """Set attribute."""
        if name not in self.db_dict:
            super(Measurement, self).__setattr__(name, value)
        else:
            tp = self.db_dict[name]['dtype']
            if value is None or isinstance(value, tp):
                super(Measurement, self).__setattr__(name, value)
            elif tp == float and isinstance(value, int):
                super(Measurement, self).__setattr__(name, float(value))
            elif tp == _np.ndarray:
                super(Measurement, self).__setattr__(
                    name, _utils.to_array(value))
            elif tp == tuple and isinstance(value, list):
                super(Measurement, self).__setattr__(name, tuple(value))
            else:
                raise TypeError('%s must be of type %s.' % (name, tp.__name__))

    def __str__(self):
        """Printable string representation of the object."""
        fmtstr = '{0:<18s} : {1}\n'
        r = ''
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                name = key[1:]
            else:
                name = key
            r += fmtstr.format(name, str(value))
        return r

    @property
    def default_filename(self):
        """Return the default filename."""
        timestamp = _utils.get_timestamp()
        filename = '{0:1s}_{1:1s}.txt'.format(timestamp, self.label)
        return filename

    def clear(self):
        """Clear measurement."""
        for key in self.__dict__:
            self.__dict__[key] = None
        return True

    def copy(self):
        """Return a copy of the object."""
        _copy = type(self)()
        for key in self.__dict__:
            if isinstance(self.__dict__[key], _np.ndarray):
                _copy.__dict__[key] = _np.copy(self.__dict__[key])
            elif isinstance(self.__dict__[key], list):
                _copy.__dict__[key] = self.__dict__[key].copy()
            else:
                _copy.__dict__[key] = self.__dict__[key]
        return _copy

    def read_file(self, filename):
        """Read measurement from file.

        Args:
        ----
            filename (str): configuration filepath.

        """
        data = _utils.read_file(filename)
        for name in self.db_dict:
            tp = self.db_dict[name]['dtype']
            value_str = _utils.find_value(data, name)
            if value_str == _empty_str:
                setattr(self, name, None)
            else:
                if tp in (_np.ndarray, list, tuple, dict):
                    value = _json.loads(_utils.find_value(data, name))
                    if tp == _np.ndarray:
                        value = _utils.to_array(value)
                else:
                    value = _utils.find_value(data, name, vtype=tp)
                setattr(self, name, value)
        return True

    def save_file(self, filename):
        """Save measurement to file."""
        if not self.valid_data():
            message = 'Invalid Data.'
            raise MeasurementError(message)

        try:
            timestamp_split = _utils.get_timestamp().split('_')
            date = timestamp_split[0]
            hour = timestamp_split[1].replace('-', ':')

            if hasattr(self, 'date') and self.date is None:
                self.date = date

            if hasattr(self, 'hour') and self.hour is None:
                self.hour = hour

            with open(filename, mode='w') as f:
                if len(self.label) != 0:
                    line = "# {0:s}\n\n".format(self.label)
                    f.write(line)

                for name in self.db_dict:
                    value = getattr(self, name)

                    if value is None:
                        value = _empty_str

                    else:
                        tp = self.db_dict[name]['dtype']
                        if tp in (_np.ndarray, list, tuple, dict):
                            if tp == _np.ndarray:
                                value = value.tolist()
                            value = _json.dumps(value).replace(' ', '')
                        elif tp == str:
                            if len(value) == 0:
                                value = _empty_str
                            value = value.replace(' ', '_')

                    line = '{0:s}\t{1}\n'.format(name.ljust(30), value)
                    f.write(line)
            return True

        except Exception:
            message = 'Failed to save measurement to file: "%s"' % filename
            raise MeasurementError(message)

    def valid_data(self):
        """Check if parameters are valid."""
        al = [
            getattr(self, name) for name in self.db_dict
            if self.db_dict[name]['not_null']
            and name not in ['idn', 'date', 'hour']]
        return all([a is not None for a in al])


class StretchedWireMeas(Measurement):
    """Stretched Wire measurements class."""

    label = 'Stretched Wire Measurement'
    collection_name = 'measurements'
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
        self.first_integral = ''
        self.second_integral = ''
        super().__init__()

    def first_integral_calculus(self):
        pass

    def second_integral_calculus(self):
        pass
