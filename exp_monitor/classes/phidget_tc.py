#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 11:00:08 2021

@author: jp

Implements the Phidget TC Class for experiment monitoring.
"""

# Standard library imports:
from Phidget22.Devices import TemperatureSensor

# Local imports:
from exp_monitor.classes.sensor import Sensor


class PhidgetTC(Sensor):

    def __init__(self, descr, hub_port, hub_channel):
        self.type = 'Thermocouple'
        self.unit = '°C'
        self.conversion_fctn = None
        self.hub_serial = 561242
        self.descr = descr.replace(' ', '_').lower() + '_temp'
        super().__init__(self.type, self.descr, self.unit, self.conversion_fctn)
        self.hub_port = hub_port
        self.hub_channel = hub_channel
        self.ts_handle = TemperatureSensor.TemperatureSensor()
        # Set addressing parameters to specify which channel to open:
        self.ts_handle.setHubPort(self.hub_port)
        self.ts_handle.setDeviceSerialNumber(self.hub_serial)
        self.ts_handle.setChannel(self.hub_channel)

    def connect(self):
        # Open Phidgets and wait for attachment:
        self.ts_handle.openWaitForAttachment(1000)

    def disconnect(self):
        # Close Phidgets:
        self.ts_handle.close()

    def measure(self, verbose=False):
        # Open:
        self.connect()
        # Receive temperature value:
        self.measurement = self.ts_handle.getTemperature()
        # Print measurement:
        if verbose:
            print(self.descr, self.measurement, self.unit)
        # Close:
        self.disconnect()

    def to_json(self):
        return super().to_json()


# Execution:
if __name__ == '__main__':

    from exp_monitor.config import tc1, tc2, tc3, tc4, tc5, tc6
    for tc in [tc1, tc2, tc3, tc4, tc5, tc6]: tc.measure(verbose=True)
