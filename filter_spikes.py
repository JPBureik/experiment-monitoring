#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Filter spikes in time-stamped dataseries for experiment monitoring with
Arduino.

Takes the output from the script unit_conv.py and checks for spikes in the
measured and converted data. If a spike is detected, the boolean write_to_db
is set to False.
"""

def filter_spikes(output_list):

    from influxdb import InfluxDBClient

    # Define limit for definition of spike in data:
    spike_factor = 10

    # Initialize Boolean:
    write_to_db = True

    # Connect to database:
    client = InfluxDBClient(host='localhost', port=8086, database='helium2')
    
    # Get all measurement series to loop over:
    series_result = client.query('SHOW series').raw
    series_list = [series_result['series'][0]['values'][i][0].split(',')[0] for i in range(len(series_result['series'][0]['values']))]

    for series in series_list:

        # Load last data point:
        ldp_result = client.query('SELECT LAST("value") FROM "{}"'.format(series)).raw
        ldp = ldp_result['series'][0]['values'][0][1]

        # Check if new datapoint == spike:
        for entry in range(len(output_list)):
            if output_list[entry]['measurement'] == series:
                if output_list[entry]['value'] > ldp * spike_factor or output_list[entry]['value'] < ldp / spike_factor:
                    write_to_db = False

    return write_to_db