#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 12:44:39 2022

Testing module for Phidgets class.

@author: jp
"""

import os

import pytest


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Requires physical Phidget hardware"
)
def test_lab_temp_phidget(lab_temp_phidget):
    """Test that Phidget measurement returns correct values."""
    lab_temp_phidget.measure()
    assert isinstance(lab_temp_phidget.measurement, float)
