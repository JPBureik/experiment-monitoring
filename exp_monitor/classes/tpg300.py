#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:50:14 2021

@author: jp

Implements the TPG 300 Class for experiment monitoring.
"""

# Local imports:
from exp_monitor.classes.sensor import Sensor
from exp_monitor.adc.arduino_adc import ArduinoADC
from exp_monitor.calibrations.calib import Calibrator


class TPG300(Sensor):

    def __init__(self, descr, adc_analog_in):
        self.type = 'Vacuum Gauge'
        self.unit = 'mbar'
        self.descr = self.descr = descr.replace(' ', '_').lower() + '_pressure'
        self.arduino_channel = adc_analog_in
        self._calib = Calibrator()
        self.conversion_fctn = self._calib.calib_fctn
        super().__init__(self.type, descr, self.unit, self.conversion_fctn)

    def measure(self, verbose=False):
        arduino_adc = ArduinoADC()
        voltage = arduino_adc.measure()[self.arduino_channel]
        self.measurement = self.conversion_fctn(voltage)
        if verbose:
            print(self.descr, self.measurement, self.unit)


# Execution:
if __name__ == '__main__':

    from exp_monitor.config import sc_vac
    sc_vac.measure(verbose=True)
