#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 12:33:08 2021

@author: jp

Implements the abstract Sensor Class for experiment monitoring.

All interfaces for acquiring data should be subclasses that inherit from this
class.
"""

# Standard library imports:
from pathlib import Path

class Sensor:

    def __init__(self, type, descr, unit, conversion_fctn):
        self.type = type  # str
        self.descr = descr  # str
        self.unit = unit  # str
        self.conversion_fctn = conversion_fctn  # function_object
        self._bounds = None  # {'lower': float, 'upper': float}
        self._filter_spikes = None  # float
        self._alert = None  # {'value': float, 'duration': float [min]}
        self._alert_cond = None  # {'value': float, 'duration': float [min]}
        self._path = Path(".")

    @property
    def bounds(self):
        """Set bounds to limit the range of incoming measured values."""
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        self._bounds = bounds

    @property
    def alert(self):
        """Set value and duration for automatic alerts."""
        return self._alert

    @alert.setter
    def alert(self, alert):
        self._alert = alert

    @property
    def filter_spikes(self):
        """Set value for spike filetring."""
        return self._filter_spikes

    @filter_spikes.setter
    def filter_spikes(self, filter_spikes):
        self._filter_spikes = filter_spikes

    def initialize(self):
        """Open the connection to the sensor."""
        pass

    def close(self):
        """Open the connection to the sensor."""
        pass

    def measure(self):
        """Return the received measurement values from sensor."""
        pass

    def conversion(self, value):
        """Perform conversion to proper unit."""
        return self._conversion_fctn(value)

    def to_json(self):
        """Return dict w/ measurement for JSON to store in influxDB."""
        pass
