#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:50:43 2021

@author: jp

Phidgets communication module.

Retrieves the values of the connected phidgets and returns them in a list.
"""


def temp_meas():

    from Phidget22.Devices import TemperatureSensor

    def onTemperatureChange(temperature):
        print("Temperature: " + str(temperature))

    # Create your Phidget channels
    temperatureSensor0 = TemperatureSensor.TemperatureSensor()

    # Set addressing parameters to specify which channel to open (if any)
    temperatureSensor0.setHubPort(4)
    temperatureSensor0.setDeviceSerialNumber(561242)

    # Open your Phidgets and wait for attachment
    temperatureSensor0.openWaitForAttachment(1000)

    temp = temperatureSensor0.getTemperature()

    # Close your Phidgets once the program is done.
    temperatureSensor0.close()

    source_temp = {}
    source_temp['measurement'] = 'source_temp'
    source_temp['unit'] = '°C'
    source_temp['phidget_hub'] = 4
    source_temp['phidget_serial'] = 561242
    source_temp['raw'] = temp
    source_temp['value'] = temp

    return source_temp


if __name__ == '__main__':

    source_temp = temp_meas()
    print(source_temp['value'])
