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


# 1 -- Define bounds for incoming data:
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
bounds['water_temp'] = {
    'lower': 5,
    'upper': 30
    }
bounds['primary_vac'] = {
    'lower': 1e-5,
    'upper': 2e3
    }
