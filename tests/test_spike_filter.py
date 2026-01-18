#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for spike filter utility functions."""

import datetime

from expmonitor.utilities.spike_filter import SpikeFilter


class TestPercentChange:
    """Tests for SpikeFilter.percent_change static method."""

    def test_percent_change_increase(self) -> None:
        """Test percent change for increasing values."""
        assert SpikeFilter.percent_change(110, 100) == 10.0

    def test_percent_change_decrease(self) -> None:
        """Test percent change for decreasing values."""
        assert SpikeFilter.percent_change(90, 100) == 10.0

    def test_percent_change_same(self) -> None:
        """Test percent change for identical values."""
        assert SpikeFilter.percent_change(100, 100) == 0.0

    def test_percent_change_zero_previous(self) -> None:
        """Test percent change when previous value is zero."""
        assert SpikeFilter.percent_change(100, 0) == float("inf")

    def test_percent_change_double(self) -> None:
        """Test percent change for doubling."""
        assert SpikeFilter.percent_change(200, 100) == 100.0


class TestConvToUTime:
    """Tests for SpikeFilter.conv_to_u_time static method."""

    def test_conv_to_u_time_format(self) -> None:
        """Test that output has correct format (19 digits)."""
        dt = datetime.datetime(2021, 4, 27, 8, 28, 0)
        result = SpikeFilter.conv_to_u_time(dt)
        assert len(result) == 19
        assert result.endswith("000000000")

    def test_conv_to_u_time_is_string(self) -> None:
        """Test that output is a string."""
        dt = datetime.datetime(2021, 4, 27, 8, 28, 0)
        result = SpikeFilter.conv_to_u_time(dt)
        assert isinstance(result, str)
