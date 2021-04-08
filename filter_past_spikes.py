#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Filter past spikes in time-stamped dataseries for experiment monitoring with
Arduino.

Takes the output from the script unit_conv.py and checks for spikes in the
measured and converted data. If a spike is detected, the boolean write_to_db
is set to False.
"""
#%%
import pickle
import time
import datetime
from influxdb import InfluxDBClient

spike_times = pickle.load(open("spike_times.p", "rb" ))

spike_utimes = {}

for series in spike_times.keys():
    spike_utimes[series] = []
    for i in range(len(spike_times[series])):
        spike_time = spike_times[series][i].strip('Z').replace('T', ' ')
        spike_datetime = datetime.datetime.strptime(spike_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=2)
        spike_utime = time.mktime(spike_datetime.timetuple())
        spike_utime_str = str(spike_utime)[:-2] + 9 * '0'
        spike_utimes[series].append(spike_utime_str)

client = InfluxDBClient(host='localhost', port=8086, database='helium2')

for series in spike_utimes.keys():
    for spike in spike_utimes[series]:
        client.query('DELETE FROM "{}" WHERE time = {}'.format(series, spike))

