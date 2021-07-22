#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:02:49 2021

@author: jp

Service script that is run continously by Linux Systemd. It executes the
specified function at the rate given by the specified interval.
"""

# Standard library imports:
import time

# Local imports:
from exp_monitor.config import *

# Specify interval in seconds:
interval = 15

# Get all user-defined objects:
user_objects = {}
for name in dir():
    value = globals()[name]
    if 'exp_monitor.classes.' in str(type(value)):
        user_objects[name] = value

# Execute measure method for every user-defined object:
while True:

    for data_source in user_objects:
        data_source.measure(verbose=True)
    time.sleep(interval)
