#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:12:52 2020

@author: jp
"""

from lxml import html
import requests
import datetime
import csv

arduino_ip = 'http://10.117.53.45'
analog_read_resolution = 12 # in bits
board_voltage = 3.3 # in V
numerical_precision = 3 # places after decimal for analog voltage values
sensor_type = 'analog'
number_of_used_analog_inputs = 2 # how many analog voltage are being measured
number_of_total_analog_inputs = 12 # Arduino Due

# Get data from Arduino web server
page = requests.get(arduino_ip)
tree = html.fromstring(page.content)

# Receive values from all configured analog sensors
sensor_label_tree_str = "//arduino_due/sensor[@type=\'" + sensor_type + "\']/text()"
sensor_reading_tree_str = '//arduino_due/sensor[@reading]/text()'
sensor_label = tree.xpath(sensor_label_tree_str)
sensor_reading = tree.xpath(sensor_reading_tree_str)

# Save measurement data for each sensor in dict
measurement = {}

for i in range(number_of_used_analog_inputs):

    # Conversion of sensor name from numeric
    sensor_conv = int(sensor_label[i])
    sensor_conv = "A" + str(sensor_conv)

    # Conversion of voltage from digital to analog
    voltage = int(sensor_reading[i]) * board_voltage / 2**analog_read_resolution
    voltage = round(voltage, numerical_precision)

    # Write to dict
    measurement[sensor_conv] = voltage

# Format for csv
fieldnames = []
fieldnames.append('Time')
for sensor in range(number_of_total_analog_inputs):
    fieldnames.append('AnalogIn' + str(sensor))

new_entry_csv = {}
new_entry_csv['Time'] = datetime.datetime.now().strftime("%m/%d %H:%M")
for sensor in range(number_of_total_analog_inputs):
    if sensor < number_of_used_analog_inputs:
        new_entry_csv[fieldnames[sensor+1]] = measurement['A' + str(sensor)] # Double check for correct sensor label
    else:
        new_entry_csv[fieldnames[sensor+1]] = '-'

# Write to csv
with open('exp_surv.csv', mode='a') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # writer.writeheader()
    writer.writerow(new_entry_csv)
