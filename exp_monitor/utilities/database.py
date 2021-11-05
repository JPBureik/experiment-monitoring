#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 10:15:47 2021

@author: jp

Implements the base class Database for experiment monitoring.

The abstract Sensor class inherits from this class to write measurement data to
the database. It is currently set up to use InfluxDB.
"""

# Standard library imports:
from influxdb import InfluxDBClient
from datetime import datetime


class Database():

    def __init__(self):
        pass

    def write(self, descr, unit, measurement, save_raw=False, raw=None):
        pass


class InfluxDBDatabase(Database):

    def __init__(self, hostname, port, db_name, **kwargs):
        super().__init__(**kwargs)
        self.client = InfluxDBClient(host=hostname, port=port, database=db_name)

    def write(self, descr, unit, measurement, save_raw=False, raw=None):
        """Write measurement result to InfluxDB database."""
        json_dict = {}
        json_dict['measurement'] = descr
        json_dict['tags'] = {}
        json_dict['tags']['unit'] = unit
        # Grafana assumes UTC:
        json_dict['time'] = datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")
        json_dict['fields'] = {}
        json_dict['fields']['value'] = measurement
        if save_raw:
            json_dict['fields']['raw'] = raw
        self.client.write_points([json_dict])
