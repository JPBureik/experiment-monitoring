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
        # General sensor setup:
        self.type = 'Vacuum Gauge'
        self.descr = descr.replace(' ', '_').lower() + '_vac'  # Multi-word
        self.unit = 'mbar'
        self._calib = Calibrator()
        self.conversion_fctn = self._calib.calib_fctn
        self.arduino_adc = ArduinoADC()
        self.num_prec = None #  self.arduino_adc.num_prec
        super().__init__(self.type, self.descr, self.unit, self.conversion_fctn,
                         self.num_prec)
        # TPG261-specific setup:
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

    from exp_monitor.config import sc_vac
    sc_vac.measure(verbose=True)
