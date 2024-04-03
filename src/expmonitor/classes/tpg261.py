#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:09:53 2021

@author: jp

Implements the TPG 261 Class for experiment monitoring.
"""

# Standard library imports:
import serial  # pip3 install pyserial

# Local imports:
from expmonitor.classes.sensor import Sensor


class TPG261(Sensor):

    def __init__(self, descr, port):
        # General sensor setup:
        self.type = 'Vacuum Gauge'
        self.descr = descr.replace(' ', '_').lower() + '_vac'  # Multi-word
        self.unit = 'mbar'
        self.conversion_fctn = lambda p: float(str(p).split(',')[1])
        super().__init__(self.type, self.descr, self.unit, self.conversion_fctn)
        # TPG261-specific setup:
        self.baudrate = 9600
        self.timeout = 1
        self.port = port

    def connect(self):
        """Not needed, handled by context manager in self.rcv_vals()."""
        pass

    def disconnect(self):
        """Not needed, handled by context manager in self.rcv_vals()."""
        pass

    def rcv_vals(self):
        # Receive pressure value as bytes:
        with serial.Serial(self.port, baudrate=self.baudrate,
                           timeout=self.timeout) as ser:
            serial_rcv = ser.readline()
        return serial_rcv



# Execution:
if __name__ == '__main__':

    from expmonitor.config import *
    TPG261.test_execution()
