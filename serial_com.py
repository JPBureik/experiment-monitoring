#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:09:53 2021

@author: jp
"""

import serial  # pip3 install pyserial

def tpg261_meas(port):

    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        
        serial_rcv = ser.readline()
        pressure = float(str(serial_rcv).split(',')[1])
        
        # Create dict for JSON:
        source_vac = {}
        source_vac['measurement'] = 'source_vac'
        source_vac['unit'] = 'mbar'
        source_vac['raw'] = pressure
        source_vac['value'] = pressure
                
    return source_vac

if __name__ == '__main__':

    source_vac = tpg261_meas('/dev/ttyUSB0')
    print(source_vac['measurement'], source_vac['value'], source_vac['unit'])