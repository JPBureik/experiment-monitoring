#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Filter past spikes in time-stamped dataseries for experiment monitoring with
influxdb.

Checks the influxdb database for spikes in past data based on a predefined
intervall for each parameter. All detected spikes can be deleted by setting
the corresponding flag before execution.
"""

# Standard library imports
import time
import datetime
from influxdb import InfluxDBClient
import multiprocessing


""" USER INPUT """

# Specify limit for definition of spike in data:
accepted_range = {}
accepted_range['sc_vac'] = {'lower': 1e-11, 'upper': 4e-9}  # mbar, no calib
accepted_range['lab_temperature'] = {'lower': 15, 'upper': 30}  # deg C


class SpikeFilter:

    def __init__(self, accepted_range):
        self.accepted_range = accepted_range
        self.series_list = []  # list(self.accepted_range.keys())
        self.data = {}
        self.timestamps = {}
        self.spike_indices = {}
        self.spike_timestamps = {}
        self.spike_utimestamps = {}
        self.total_spikes = {}
        self.set_database()
        self.display_series()
        self.set_accepted_range()

    @staticmethod
    def is_inbounds(data_point, lower_bound, upper_bound, inclusive=True):
        if inclusive:
            return True if lower_bound <= data_point <= upper_bound else False
        else:
            return True if lower_bound < data_point < upper_bound else False

    @staticmethod
    def conv_to_u_time(date_time):
        # date_time = date_time + datetime.timedelta(hours=2)
        u_time = time.mktime(date_time.timetuple())
        u_time_str = str(u_time)[:-2] + 9 * '0'
        return u_time_str

    def set_database(self):
        self.database = input('Specify database:\n')
        self.client = InfluxDBClient(host='localhost', port=8086,
                                     database=self.database)

    def set_accepted_range(self):
        pass

    def display_series(self):
        series_result = self.client.query('SHOW series').raw
        self.series_list = [series_result['series'][0]['values'][i][0].
                            split(',')[0] for i in
                            range(len(series_result['series'][0]['values']))]
        print('Measurement series in {}: '.format(self.database))
        for series in self.series_list:
            print('\t', series)

    def find_spikes(self, series):
        # Get data:
        data_result = self.client.query(
            'SELECT * FROM "{}"'.format(series)
            ).raw
        self.data[series] = [data_result['series'][0]['values'][i][-1] for i in
                             range(len(data_result['series'][0]['values']))]
        # Get timestaps:
        self.timestamps[series] = [data_result['series'][0]['values'][i][0] for
                                   i in range(len(data_result['series'][0]
                                                        ['values']))]
        # Find spike indices:
        self.spike_indices[series] = []
        for i in range(len(self.data[series])-1):
            if not self.is_inbounds(self.data[series][i],
                                    self.accepted_range[series]['lower'],
                                    self.accepted_range[series]['upper']):
                self.spike_indices[series].append(i)
        # Get timestamps at spike indices:
        self.spike_timestamps[series] = []
        for i in range(len(self.spike_indices[series])):
            self.spike_timestamps[series].append(
                self.timestamps[series][self.spike_indices[series][i]]
                )
        # Convert spike timestamp to unix time:
        self.spike_utimestamps[series] = []
        for i in range(len(self.spike_timestamps[series])):
            spike_timestamp = self.spike_timestamps[series][i].strip('Z')\
                .replace('T', ' ')
            spike_datetimestamp = datetime.datetime.strptime(
                spike_timestamp, '%Y-%m-%d %H:%M:%S') +\
                datetime.timedelta(hours=1)  # Before summer time; after: +2h
            spike_utimestamp = time.mktime(spike_datetimestamp.timetuple())
            spike_utimestamp_str = str(spike_utimestamp)[:-2] + 9 * '0'
            self.spike_utimestamps[series].append(spike_utimestamp_str)
        # Get total number of spikes:
        self.total_spikes[series] = len(self.spike_utimestamps[series])
        # Delete spikes:
        for spike in self.spike_utimestamps[series]:
            # client.query('DELETE FROM "{}" WHERE time = {}'.format(
            #   series, spike
            #   ))
            pass
        """ print this as table """
        """ ask delete via user input not flag in script """
        """ ask limits same """


""" MAIN """

if __name__ == '__main__':

    spike_filter = SpikeFilter(accepted_range)

    with multiprocessing.Pool() as pool:
        pool.map(spike_filter.find_spikes, spike_filter.series_list)

# print('Accepted range: {} -> Total spikes: {}: {}; {}: {}'.format(
#         accepted_range, series_list[0], total_spikes[series_list[0]],
#         series_list[1], total_spikes[series_list[1]]
#         ))
