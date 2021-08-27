#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:35:44 2021

@author: jp

Configuration file for experiment monitoring.

This file regroups all user input for individual setups. Enter all required
information in all sections for the proposed sensors and lab equipment below,
or feel free to add any new hardware interface you want to connect.
"""


""" ---------- GENERAL SETUP ---------- """


# Define interval for data acquisition (in seconds):
acq_interv = 15


""" ---------- SENSOR SETUP ---------- """


# Import all specific sensor classes:
from exp_monitor.classes.phidget_tc import PhidgetTC
from exp_monitor.classes.tpg261 import TPG261
from exp_monitor.adc.arduino_adc import ArduinoADC
from exp_monitor.classes.tpg300 import TPG300

# Setup Phidgets:
tc1 = PhidgetTC('Source', 4, 0)
tc2 = PhidgetTC('A/C', 4, 1)
tc3 = PhidgetTC('Lab', 4, 2)
tc4 = PhidgetTC('Water', 4, 3)
tc5 = PhidgetTC('Zeeman1', 5, 0)
tc6 = PhidgetTC('Zeeman2', 5, 1)

# Setup serial devices:
primary_vac = TPG261('Primary Pump', '/dev/ttyUSB0')

# Setup analog devices via Arduino:
sc_vac = TPG300('Science Chamber', 2)
sc_vac.bounds = {'lower': 2.34-12, 'upper': 3.45e-09}


""" ---------- DETAILS ---------- """


# Exception logging:
overwrite_log_file = True  # Replace old log file each time exec is run
log_full_tb = False  # Log entire traceback for exceptions, not just one line

# Debugging:
verbose = False  # Prints exception traceback to stdout
