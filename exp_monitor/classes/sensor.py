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
        self._bounds = None  # {'lower': float, 'upper': float}
        self._alert = False  # bool
        self._alert_value = None  # float
        self.conversion_fctn = conversion_fctn  # function_object
        self._path = PATH(".")

    @property
    def bounds(self):
        """Set bounds for measured values to filter spikes."""
        return self._bounds

    @bounds.setter
    def bounds(self, bounds):
        self._bounds = bounds

    @bounds.deleter
    def bounds(self):
        del self._bounds

    @property
    def alert(self):
        """Set bounds for measured values to filter spikes."""
        return self._bounds

    @bounds.setter
    def alert(self, bounds):
        self._bounds = bounds

    @bounds.deleter
    def alert(self):
        del self._bounds

    def conversion(self, value):
        """Perform conversion to proper unit."""
        return self._conversion_fctn(value)

    def measure(self):
        """Receive measurement values from sensor."""
        pass
