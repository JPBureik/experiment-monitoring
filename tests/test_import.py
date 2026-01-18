#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic import tests to verify package structure."""


def test_import_expmonitor():
    """Test that expmonitor package can be imported."""
    import expmonitor

    assert expmonitor is not None


def test_import_sensor():
    """Test that Sensor base class can be imported."""
    from expmonitor.classes.sensor import Sensor

    assert Sensor is not None
