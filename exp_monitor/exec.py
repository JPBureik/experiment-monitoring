#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:02:49 2021

@author: jp

Service script that is run continously by Linux Systemd. It executes the
specified function at the rate given by the specified interval.
"""

# Standard library imports:
import getpass
from pathlib import Path
import os
import glob
from datetime import date, datetime
import shutil
import time

# Local imports:
from exp_monitor.config import *

# Check for log file directory and replace old log file:
log_dir = Path('/home/' + getpass.getuser() + '/.exp_monitor')
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)
for f in glob.glob(str(log_dir) + '/log_*.txt'):
    os.remove(f)
log_file = log_dir / ('log_' + date.today().strftime('%Y_%m_%d') + '.txt')
log_file.touch()

# Continuously execute measure method for every user-defined object in config:
while True:
    for object_name in dir():
        object = globals()[object_name]
        # Identify user-defined objects:
        if 'exp_monitor.classes.' in str(type(object)):
            # Check if measure method exists:
            if callable(getattr(object, 'measure')):
                try:
                    # Make measurement:
                    object.measure()
                    # Write to database:
                    object.to_influxdb()
                # Log exceptions but continue execution:
                except Exception as e:
                    with open(log_file, 'w') as logf:
                        logf.write(
                            'Data acquisition failure for {} at {} due to {}\n'
                            .format(
                                object_name,
                                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                str(e)
                                )
                            )
    break
    time.sleep(acq_interv)
