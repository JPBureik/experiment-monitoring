#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 12:33:08 2021

@author: jp

Implements the Sensor Class for experiment monitoring.

All interfaces for acquiring data can be implemented as instantiations of this
class.
"""


class Sensor:

    def __init__(self, type, descr, conversion_fctn):
        self.type = type
        self.descr = descr
        self._bounds = None
        self._conversion_fctn = conversion_fctn

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

    def conversion(self, value):
        """Perform conversion to proper unit."""
        return self._conversion_fctn(value)
