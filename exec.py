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
from influxdb_write import influxdb_write

# Specify intervall in seconds:
interval = 1

# Main loop:
while True:

    influxdb_write()
    time.sleep(interval)
