#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:09:53 2021

@author: jp

Serial communication module for receiving measurement values from TPG 261.

Takes the serial port as string and returns the measurement value in a dict
for JSON to be stored in influxDB.
"""

# Standard library imports:
import serial  # pip3 install pyserial


def tpg261_meas(port):

    with serial.Serial(port, baudrate=9600, timeout=1) as ser:

        # Receive measurement bytes from gauge:
        serial_rcv = ser.readline()

    # Convert to float:
    pressure = float(str(serial_rcv).split(',')[1])

    # Create dict for JSON:
    primary_vac = {}
    primary_vac['measurement'] = 'primary_vac'
    primary_vac['unit'] = 'mbar'
    primary_vac['raw'] = pressure
    primary_vac['value'] = pressure

    return primary_vac


if __name__ == '__main__':

    primary_vac = tpg261_meas('/dev/ttyUSB0')
    print(primary_vac['measurement'], primary_vac['value'], primary_vac['unit'])
