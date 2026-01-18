#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 11:01:07 2021

@author: jp

General utility module.

Collection of helper functions that are used in multiple scripts.
"""

from __future__ import annotations

import inspect
from typing import Any


def get_subclass_objects(BaseClass: type) -> list[Any]:
    """Get all objects that extend BaseClass from global scope of the outermost
    caller frame."""
    # Get current frame:
    f = inspect.currentframe()
    # Get globals of outermost caller frame:
    om_caller_globals = inspect.getouterframes(f)[-1].frame.f_globals
    # Get subclass objects of BaseClass:
    return [
        value
        for key, value in om_caller_globals.items()
        if issubclass(type(value), BaseClass)
    ]
