#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:02:49 2021

@author: jp

General utility module.

Collection of helper functions that are used in multiple scripts.
"""

def get_subclass_objects(BaseClass):
    """Get all objects from global scope that extend BaseClass."""
    return [value for key, value in globals().items()
            if issubclass(type(value), BaseClass)]