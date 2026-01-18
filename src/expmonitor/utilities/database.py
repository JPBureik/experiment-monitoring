#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 10:15:47 2021

@author: jp

Implements the base class Database for experiment monitoring.

The abstract Sensor class inherits from this class to write measurement data to
the database. It is currently set up to use InfluxDB.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from influxdb import InfluxDBClient


class Database:
    """InfluxDB database wrapper for sensor measurements."""

    port: int
    name: str
    client: InfluxDBClient

    def __init__(self) -> None:
        self.port = 8086
        self.name = "helium2"
        self.client = InfluxDBClient(
            host="localhost", port=self.port, database=self.name
        )

    def write(
        self,
        descr: str,
        unit: str | None,
        measurement: Any,
        save_raw: bool = False,
        raw: Any = None,
    ) -> None:
        """Write measurement result to InfluxDB database."""
        json_dict: dict[str, Any] = {
            "measurement": descr,
            "tags": {"unit": unit},
            "time": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
            "fields": {"value": measurement},
        }
        if save_raw:
            json_dict["fields"]["raw"] = raw
        self.client.write_points([json_dict])
