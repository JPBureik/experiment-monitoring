#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:12:52 2020

@author: jp
"""

from lxml import html
import requests

arduino_ip = 'http://192.168.1.19'
analog_read_resolution = 12 # in bits
board_voltage = 3.3 # in V
numerical_precision = 3 # places after decimal for analog voltage values
sensor_type = 'analog'
number_of_analog_inputs = 2 # how many analog voltage are being measured

page = requests.get(arduino_ip)
tree = html.fromstring(page.content)

# Receive values from all configured analog sensors
sensor_tree_str = "//arduino_due/sensor[@type=\'" + sensor_type + "\']/text()"
reading_tree_str = '//arduino_due/sensor[@reading]/text()'
sensor = tree.xpath(sensor_tree_str)
reading = tree.xpath(reading_tree_str)

# Save in dict
values = {}

for i in range(number_of_analog_inputs):

    # Conversion of sensor name from numeric
    sensor_conv = int(sensor[i])
    sensor_conv = "A" + str(sensor_conv)
    
    # Conversion of voltage from digital to analog
    voltage = int(reading[i]) * board_voltage / 2**analog_read_resolution
    voltage = round(voltage, numerical_precision)

    # Write to dict
    values[sensor_conv] = voltage
    
print(values)