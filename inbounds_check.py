#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 15:37:44 2021

@author: jp

Bounds for incoming data and a function to check them for data acquisition in
experiment monitoring.

Stores user defined bounds in a dict and checks whether new incoming data is
inbounds for each parameter.
"""


# Define bounds for incoming data:
bounds = {}
bounds['lab_temp'] = {
    'lower': 15,
    'upper': 30
    }
bounds['sc_vac'] = {
    'lower': 2.3410943978374387e-12,
    'upper': 3.442785879172718e-09
    }
bounds['source_temp'] = {
    'lower': -200,
    'upper': 30
    }
bounds['a/c_temp'] = {
    'lower': 15,
    'upper': 30
    }
bounds['primary_vac'] = {
    'lower': 1e-5,
    'upper': 2e3
    }


# Inbounds check:
def is_inbounds(data_point, lower_bound, upper_bound, inclusive=True):
    if inclusive:
        return True if lower_bound <= data_point <= upper_bound else False
    else:
        return True if lower_bound < data_point < upper_bound else False
