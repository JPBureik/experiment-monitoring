#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 08 12:07:49 2022

Fixtures for all testing modules.

@author: jp
"""

import os

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "hardware: mark test as requiring hardware")


def pytest_collection_modifyitems(config, items):
    """Skip hardware tests in CI."""
    if os.environ.get("CI") != "true":
        return
    skip_hardware = pytest.mark.skip(reason="Requires physical hardware")
    for item in items:
        if "hardware" in item.keywords:
            item.add_marker(skip_hardware)


@pytest.fixture(scope="session")
def lab_temp_phidget(request):
    """Return sensor object for lab temp phidget."""
    if os.environ.get("CI") == "true":
        pytest.skip("Requires physical Phidget hardware")
    from expmonitor.classes.phidget_tc import PhidgetTC

    tc3 = PhidgetTC("Lab", 4, 2)
    return tc3
