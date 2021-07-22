#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:50:14 2021

@author: jp

Implements the TPG 300 Class for experiment monitoring.
"""

# Local imports:
from exp_monitor.classes.sensor import Sensor
from exp_monitor.classes.arduino_adc import ArduinoADC

class TPG300(Sensor):

    def __init__(self, descr):
        self.type = 'Vacuum Gauge'
        self.unit = 'mbar'
        self.arduino_ai = 1
        self.conversion_fctn = None
        super().__init__(self.type, descr, self.unit, self.conversion_fctn)

    def measure(self, verbose=False):
        arduino_adc = ArduinoADC()
        voltage = arduino_adc.measure(self.arduino_ai)
