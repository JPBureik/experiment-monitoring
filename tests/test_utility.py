#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for utility module."""

from expmonitor.utilities.utility import get_subclass_objects


class TestGetSubclassObjects:
    """Tests for get_subclass_objects function."""

    def test_returns_list(self) -> None:
        """Test that function returns a list."""
        # The function inspects the outermost caller frame's globals,
        # which in pytest context won't find our test objects.
        # We can only verify it returns a list without errors.
        results = get_subclass_objects(object)
        assert isinstance(results, list)
