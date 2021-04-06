#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:36:28 2020

@author: jp

Python interface for influDB databases.

Takes a list of floats or ints and writes them into a specified inflluxDB
database.
"""

from influxdb import InfluxDBClient
from datetime import datetime


from eth_com import rcv_meas
from unit_conv import unit_conv

now = datetime.utcnow() # Grafana assumes UTC
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

analog_signals = rcv_meas()
output_list, write_to_db = unit_conv(analog_signals)

Nport = 8086

client = InfluxDBClient(host='localhost', port=8086, database='helium2')

json_body = []
for i in range(2):
    json_body.append(
        {
            "measurement": output_list[i]['measurement'],
            "tags": {
                "unit": output_list[i]['unit'],
            },
            "time": dt_string,
            "fields": {
                "value": output_list[i]['value'],
                "raw": analog_signals[i],
            }
        }
    )

if write_to_db is True:
    client.write_points(json_body)
