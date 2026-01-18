#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 08 12:07:49 2022

Fixtures for all testing modules.

@author: jp
"""

import os

import pytest


@pytest.fixture(scope="session")
def lab_temp_phidget():
    """Return sensor object for lab temp phidget."""
    if os.environ.get("CI") == "true":
        pytest.skip("Requires physical Phidget hardware")
    from expmonitor.classes.phidget_tc import PhidgetTC
    tc3 = PhidgetTC('Lab', 4, 2)
    return tc3
