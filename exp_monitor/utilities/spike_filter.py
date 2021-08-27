#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 10:00:50 2021

@author: jp

Module to filter spikes in incoming data.

Checks the new incoming value versus the last value(s) and determines if the
last value was a spike.
"""

# Local imports
from exp_monitor.utilities.database import Database


class SpikeFilter():

    def __init__(self):
        self._spike_threshold = None  # float (0,1)
        self._spike_length = 1  # int
        self._disabled = False  # Disable spike filter if spike length too long
    
    @property
    def spike_threshold(self):
        """The percentage value that a data point has to deviate from the
         others by in order to be qualified as a spike."""
        return self._spike_threshold

    @spike_threshold.setter
    def spike_threshold(self, spike_threshold):
        if type(spike_threshold) == float and 0. < spike_threshold < 1.:
            self._spike_threshold = spike_threshold

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
            raise ValueError(""""
            Large spike lengths can silence legitimate alert conditions.
            Spike filter disabled""")
            self._disabled = True

    def db_setup():
        pass
    

    def filter_spikes(incoming_data, previous_data):
        # Get previous data to compare to incoming:
            pass