#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Live spike filter for incoming data.

Checks the new incoming value versus the last data, determines if there was a
spike and if so, deletes it.
"""

# Standard library imports
import numpy as np
import pandas as pd
import datetime
import time

# Local imports
from exp_monitor.utilities.database import Database


class SpikeFilter():

    def __init__(self, sensor, spike_threshold_perc, spike_length=1):
        self.sensor = sensor  # Object extending the Sensor class
        self.spike_threshold_perc = spike_threshold_perc  # Percentage
        self.spike_length = spike_length  # int
        self.enabled = False  # Enable by setting spike_threshold_perc

    @property
    def spike_threshold_perc(self):
        """The percentage value that a data point has to deviate from the
         others by in order to be qualified as a spike."""
        return self._spike_threshold_perc

    @spike_threshold_perc.setter
    def spike_threshold_perc(self, spike_threshold_perc):
        if type(spike_threshold_perc) in [int, float]:
            self._spike_threshold_perc = abs(spike_threshold_perc)
            self.enabled = True
        else:
            self._spike_threshold_perc = None

    @property
    def spike_length(self):
        """Length of spike. Generally 1 or 2 will suffice. Risk of silencing
        legitimate alert conditions if increased beyond 4."""
        return self._spike_length

    @spike_length.setter
    def spike_length(self, spike_length):
        if type(spike_length) == int and spike_length < 5:
            self._spike_length = spike_length
        elif type(spike_length) == int and spike_length > 4:
            raise ValueError(""""Large spike lengths can silence legitimate"""
                             + """ alert conditions.\nSpike filter disabled.""")
            self.enabled = False

    @staticmethod
    def percent_change(current, previous):
        """Return change between current and previous in percent."""
        try:
            return (abs(current - previous) / previous) * 100
        except ZeroDivisionError:
            return float('inf')

    @staticmethod
    def conv_to_u_time(date_time):
        """Convert date_time to unix time."""
        date_time = date_time + datetime.timedelta(hours=2)
        u_time = time.mktime(date_time.timetuple())
        u_time_str = str(u_time)[:-2] + 9 * '0'
        return u_time_str

    def was_spike(self):
        """Check if preceeding values around spike_length in the measurement
        series fullfill spike conditions."""
        query_result = self.sensor._db.client.query(
            'SELECT * FROM {} GROUP BY * ORDER BY DESC LIMIT {}'.format(
                self.sensor.descr, self._spike_length + 2)).raw
        df = pd.DataFrame(
            query_result['series'][0]['values'], columns=['Timestamp', 'Value']
        )
        df = df.sort_values(by='Timestamp')
        self._spike_range = df.iloc[df.index[1:-1]]
        baseline = df.drop(self._spike_range.index)
        if self.percent_change(np.mean(self._spike_range['Value']),
                               np.mean(baseline['Value'])) >= self.spike_threshold_perc:
            return True
        else:
            return False

    def del_spike(self):
        """Delete datapoints identified as spike from the database."""
        # Create unix timestamps for spike datapoints:
        spike_timestamps = [datetime.datetime.strptime(
            self._spike_range['Timestamp'].values[i], '%Y-%m-%dT%H:%M:%SZ'
        ) for i in range(len(self._spike_range.index))]
        spike_utimestamps = [self.conv_to_u_time(spike_timestamp) for
                             spike_timestamp in spike_timestamps]
        # Delete database entries at spike unix timestamps:
        for spike_utime in spike_utimestamps:
            self.sensor._db.client.query(
                'DELETE FROM "{}" WHERE time = {}'.format(self.sensor.descr,
                                                          spike_utime)
            )
