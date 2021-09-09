#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 12:33:08 2021

@author: jp

Implements the abstract base class Sensor for experiment monitoring.

All interfaces for acquiring data should be subclasses that inherit from this
class.
"""

# Standard library imports:
from abc import ABC, abstractmethod
from influxdb import InfluxDBClient
import traceback

# Local imports
from exp_monitor.utilities.database import Database


class Sensor(ABC):

    """ ---------- INIT ---------- """


    def __init__(self, type, descr, unit, conversion_fctn, num_prec=None,
                 save_raw=False, format_str='f'):
        self.type = type  # str
        self.descr = descr  # str
        self.unit = unit  # str
        self.conversion_fctn = conversion_fctn  # function_object
        self.num_prec = num_prec  # Set numerical precision
        self.save_raw = save_raw  # bool
        self.format_str = format_str  # 'f': float, 'i': int, 's': str
        # Database setup:
        self._db = Database()


    """ ---------- PROPERTIES ---------- """


    @property
    def num_prec(self):
        """Set numerical precision for measurement values.
        For example, num_prec = 12 saves 1.2381e-10 as 1.24e-10."""
        return self._num_prec

    @num_prec.setter
    def num_prec(self, num_prec):
        if type(num_prec) == int and num_prec > 0:
            self._num_prec = num_prec
        else:
            self._num_prec = None

    @property
    def format_str(self):
        """Set format in which to save measurement data. Currently all data
        within one influxDB shard needs to be of the same format."""
        return self._format_str

    @format_str.setter
    def format_str(self, format_str):
        self._format_dict = {'f': float, 'i': round, 's': str}
        if format_str in self._format_dict.keys():
            self._format_str = format_str
        else:
            self._format_str = 'f'

    @property
    def save_raw(self):
        """Save raw measurement data as received from sensor (before conversion
        and formatting) to database."""
        return self._save_raw

    @save_raw.setter
    def save_raw(self, save_raw):
        if type(save_raw) == bool:
            self._save_raw = save_raw
        else:
            self._save_raw = False


    """ ---------- ABSTRACT METHODS ---------- """


    @abstractmethod
    def connect(self):
        """Open the connection to the sensor."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection to the sensor."""
        pass

    @abstractmethod
    def rcv_vals(self):
        """Receive and return measurement values from sensor."""
        pass  # return received_vals


    """ ---------- PRIVATE METHODS ---------- """


    def _show(self, show_raw=False):
        """Print last measurement with description and units."""
        try:
            if show_raw:
                print(self.descr, self.measurement, self.unit, ';\t raw:',
                      self.raw_vals)
            else:
                print(self.descr, self.measurement, self.unit)
        except AttributeError as ae:
            print(self.descr, '_show AttributeError:', ae.args[0])

    def _apply_num_prec(self, value):
        """Apply numerical precision to value."""
        try:
            return float('{:.{}f}'.format(float(value), self._num_prec))
        except (ValueError, TypeError):
             return value

    def _apply_format(self, value):
        """Apply format to value."""
        try:
            return self._format_dict[self._format_str](value)
        except ValueError:
            return value

    def _convert(self, value):
        """Perform conversion of received values to proper unit."""
        try:
            return self.conversion_fctn(value)
        except (TypeError, ValueError):
            return None


    """ ---------- PUBLIC METHODS ---------- """


    def measure(self, verbose=False, show_raw=False):
        """Execute a measurement."""
        self.connect()
        self.raw_vals = self.rcv_vals()
        self.measurement = self._convert(self.raw_vals)
        # Account for numerical precision and format:
        self.measurement = self._apply_num_prec(self.measurement)
        self.measurement = self._apply_format(self.measurement)
        ## SPIKE FILTER
        ## CHECK SAVE RAW DATA
        if verbose:
            self._show(show_raw)
        self.disconnect()

    def to_db(self):
        """Write measurement result to database."""
        if self._save_raw:
            self._db.write(self.descr, self.unit, self.measurement,
                           self.save_raw, self.raw)
        else:
            self._db.write(self.descr, self.unit, self.measurement)

    @classmethod
    def test_execution(cls):
        """Execute measure method for all sensors of this class defined in
        config file and print result to stdout. Has to be preceeded by the
        following import line:
        'from exp_monitor.config import *'."""
        # Import from exec module impossible at module level (cir. dependency):
        from exp_monitor.exec import get_subclass_objects
        sensor_list = get_subclass_objects(cls)
        for sensor in sensor_list:
            sensor.measure(verbose=True)
