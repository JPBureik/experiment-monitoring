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
from expmonitor.classes.sensor import Sensor


class PhidgetTC(Sensor):

    def __init__(self, descr, hub_port, hub_channel):
        # General sensor setup:
        self.type = 'Thermocouple'
        self.descr = descr.replace(' ', '_').lower() + '_temp'  # Multi-word
        self.unit = '°C'
        self.conversion_fctn = lambda t: t  # No conversion needed
        super().__init__(
            self.type, self.descr, self.unit, self.conversion_fctn, num_prec=1
            )
        # Phidget-specific setup:
        self.hub_serial = 561242
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

    def rcv_vals(self):
        # Receive temperature value:
        return self.ts_handle.getTemperature()


# Execution:
if __name__ == '__main__':

    from expmonitor.config import *
    PhidgetTC.test_execution()
