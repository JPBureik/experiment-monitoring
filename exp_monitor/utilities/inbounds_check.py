#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 15:37:44 2021

@author: jp

Bounds for incoming data and a function to check them for data acquisition in
experiment monitoring.

Checks whether new incoming data is inbounds for each parameter.
"""


# Inbounds check:
def is_inbounds(data_point, lower_bound, upper_bound, inclusive=True):
    if inclusive:
        return True if lower_bound <= data_point <= upper_bound else False
    else:
        return True if lower_bound < data_point < upper_bound else False
