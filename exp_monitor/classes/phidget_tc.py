#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 11:00:08 2021

@author: jp

Implements the Phidget TC Class for experiment monitoring.
"""

# Standard library imports:
from pathlib import Path
from Phidget22.Devices import TemperatureSensor

# Local imports:
from sensor import Sensor


class PhidgetTC(Sensor):

    def __init__(self, descr, hub_port, hub_serial, hub_channel):
        self.type = 'Thermocouple'
        self.unit = '°C'
        self.conversion_fctn = None
        super().__init__(self.type, descr, self.unit, self.conversion_fctn)
        self.hub_port = hub_port
        self.hub_serial = hub_serial
        self.hub_channel = hub_channel
        self.ts_handle = TemperatureSensor.TemperatureSensor()
        # Set addressing parameters to specify which channel to open:
        self.ts_handle.setHubPort(self.hub_port)
        self.ts_handle.setDeviceSerialNumber(self.hub_serial)
        self.ts_handle.setChannel(self.hub_channel)

    def initialize(self):
        # Open Phidgets and wait for attachment:
        self.ts_handle.openWaitForAttachment(1000)

    def close(self):
        # Close Phidgets:
        self.ts_handle.close()

    def measure(self):
        # Open:
        self.initialize()
        # Receive temperature value:
        self.measurement = self.ts_handle.getTemperature()
        # Close:
        self.close()

    def to_json(self):
        """Return dict w/ measurement for JSON to store in influxDB."""
        self.json_dict = {}
        self.json_dict['measurement'] = self.descr.lower() + '_temp'
        self.json_dict['unit'] = self.unit
        self.json_dict['value'] = self.measurement


# Execution:
if __name__ == '__main__':

    tc1 = PhidgetTC('Source', 4, 561242, 0)
    tc1.bounds = {'lower': -200, 'upper': 25}
