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

# Define limit for definition of spike in data:

accepted_range = {}
accepted_range['sc_vac'] = {'lower': 1e-11, 'upper': 4e-9}
accepted_range['lab_temperature'] = {'lower': 15, 'upper': 30}

# Connect to database:
client = InfluxDBClient(host='localhost', port=8086, database='helium2')

# Get list of measurement series:
series_result = client.query('SHOW series').raw
series_list = [series_result['series'][0]['values'][i][0].split(',')[0] for i in range(len(series_result['series'][0]['values']))]

# Get all data_
all_data = {}
for series in series_list:
    all_data_result = client.query('SELECT * FROM "{}"'.format(series)).raw
    all_data[series] = [all_data_result['series'][0]['values'][i][-1] for i in range(len(all_data_result['series'][0]['values']))]

# Find spike indices:
spike_indices = {}
for series in all_data.keys():
    spike_indices[series] = []
    for i in range(len(all_data[series])-1):
        if all_data[series][i] < accepted_range[series]['lower'] or all_data[series][i] > accepted_range[series]['upper']:
            spike_indices[series].append(i)

all_data = {}
for series in series_list:
    all_data_result = client.query('SELECT * FROM "{}"'.format(series)).raw
    all_data[series] = [all_data_result['series'][0]['values'][i][0] for i in range(len(all_data_result['series'][0]['values']))]

spike_times = {}

for series in series_list:
    spike_times[series] = []
    for i in range(len(spike_indices[series])):
        spike_times[series].append(all_data[series][spike_indices[series][i]])

# pickel.dump(spike_times, open("spike_times.p", "wb"))

# spike_times = pickle.load(open("spike_times.p", "rb" ))

spike_utimes = {}

def conv_to_u_time(date_time):
        # date_time = date_time + datetime.timedelta(hours=2)
        u_time = time.mktime(date_time.timetuple())
        u_time_str = str(u_time)[:-2] + 9 * '0'
        return u_time_str


for series in spike_times.keys():
    spike_utimes[series] = []
    for i in range(len(spike_times[series])):
        spike_time = spike_times[series][i].strip('Z').replace('T', ' ')
        spike_datetime = datetime.datetime.strptime(spike_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=1)  # Before summer time; after: +2h
        spike_utime = time.mktime(spike_datetime.timetuple())
        spike_utime_str = str(spike_utime)[:-2] + 9 * '0'
        spike_utimes[series].append(spike_utime_str)

total_spikes = {}

for series in spike_utimes.keys():
    total_spikes[series] = len(spike_utimes[series])
    for spike in spike_utimes[series]:
        client.query('DELETE FROM "{}" WHERE time = {}'.format(series, spike))

print('Accepted range: {} -> Total spikes: {}: {}; {}: {}'.format(accepted_range, series_list[0], total_spikes[series_list[0]], series_list[1], total_spikes[series_list[1]]))
