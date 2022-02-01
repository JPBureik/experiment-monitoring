#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:50:14 2021

@author: jp

Implements the TPG 300 Class for experiment monitoring.
"""

# Local imports:
from expmonitor.classes.sensor import Sensor
from expmonitor.classes.adc.arduino_adc import ArduinoADC
from expmonitor.calibrations.calib import Calibrator


class TPG300(Sensor):

    def __init__(self, descr, adc_analog_in):
        # General sensor setup:
        self.type = 'Vacuum Gauge'
        self.descr = descr.replace(' ', '_').lower() + '_vac'  # Multi-word
        self.unit = 'mbar'
        self._calib = Calibrator()
        self.conversion_fctn = self._calib.calib_fctn
        super().__init__(
            self.type, self.descr, self.unit, self.conversion_fctn, num_prec=12
            )
        # TPG261-specific setup:
        self.arduino_adc = ArduinoADC()
        self.arduino_channel = adc_analog_in

    def connect(self):
        """Open the connection to the Arduino."""
        self.arduino_adc.connect()

    def disconnect(self):
        """Close the connection to the Arduino."""
        self.arduino_adc.disconnect()

    def rcv_vals(self):
        """Receive and return measurement values from Arduino."""
        return self.arduino_adc.measure()[self.arduino_channel]


# Execution:
if __name__ == '__main__':

    from exp_monitor.config import *
    TPG300.test_execution()
