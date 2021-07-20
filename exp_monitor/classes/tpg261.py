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
from exp_monitor.classes.sensor import Sensor


class TPG261(Sensor):

    def __init__(self, descr, port):
        self.type = 'Vacuum Gauge'
        self.unit = 'mbar'
        self.baudrate = 9600
        self.timeout = 1
        self.conversion_fctn = lambda p: float(str(p).split(',')[1])
        super().__init__(self.type, descr, self.unit, self.conversion_fctn)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def measure(self, verbose=False):
        with serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout) as ser:
            # Receive measurement bytes from gauge:
            self.serial_rcv = ser.readline()
        self.measurement = super().conversion_fctn(self.serial_rcv)
        if verbose:
            print(self.descr, self.measurement, self.unit)

    def to_json(self):
        return super().to_json()


# Execution:
if __name__ == '__main__':

    from exp_monitor.config import primary_vac
    primary_vac.measure(verbose=True)
