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
from classes/influxdb_write import influxdb_write

# Specify interval in seconds:
interval = 15

# Main loop:
while True:

    influxdb_write()
    time.sleep(interval)
