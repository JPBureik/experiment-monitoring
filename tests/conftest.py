#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 08 12:07:49 2022

Fixtures for all testing modules.

@author: jp
"""

# Standard library imports:
import pytest
import os

# Local imports
from expmonitor.classes.phidget_tc import PhidgetTC
from expmonitor.classes.tpg261 import TPG261
from expmonitor.classes.tpg300 import TPG300
from expmonitor.classes.ups.eaton_ups import EatonUPS

@pytest.fixture(scope="session")
def lab_temp_phidget():
    """Return sensor object for lab temp phidget."""
    tc3 = PhidgetTC('Lab', 4, 2)
    return tc3