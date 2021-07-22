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

# Execute measure method for every user-defined object:
while True:
    for object_name in dir():
        object = globals()[object_name]
        measure = getattr(object, 'measure', None)
        if callable(measure):
            object.measure(verbose=True)
    time.sleep(acq_interv)
