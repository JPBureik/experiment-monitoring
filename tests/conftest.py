#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 08 12:07:49 2022

Fixtures for all testing modules.

@author: jp
"""

import os

import pytest

# Skip all hardware tests in CI
if os.environ.get("CI") == "true":
    collect_ignore_glob = ["test_phidgets.py"]


@pytest.fixture(scope="session")
def lab_temp_phidget():
    """Return sensor object for lab temp phidget."""
    from expmonitor.classes.phidget_tc import PhidgetTC
    tc3 = PhidgetTC('Lab', 4, 2)
    return tc3
