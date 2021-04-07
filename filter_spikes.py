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

def filter_spikes(output_list, write_to_db):
    return output_list, write_to_db