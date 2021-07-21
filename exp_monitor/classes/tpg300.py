#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:50:14 2021

@author: jp

Implements the TPG 300 Class for experiment monitoring.
"""

# Standard library imports:
import pickle
from pathlib import Path

# Local imports:
from exp_monitor.classes.sensor import Sensor

class TPG300(Sensor):

    def __init__(self, descr):
        self.type = 'Vacuum Gauge'
        self.unit = 'mbar'
        self.arduino_ai = 1
        self.conversion_fctn = None
        super().__init__(self.type, descr, self.unit, self.conversion_fctn)
        self.arduino_store = Path("exp_monitor/adc/analog_signals.p")

    def measure(self, verbose=False):
        try:
            my_abs_path = my_file.resolve(strict=True)
        except FileNotFoundError:
            print('Initialize Arduino!')
            self.measurement = None
        else:
            self.measurement = pickle.load(self.arduino_store)[self.arduino_ai]
        if verbose:
            print(self.descr, self.measurement, self.unit)
