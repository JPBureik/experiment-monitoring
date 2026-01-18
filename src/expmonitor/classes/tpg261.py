#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:09:53 2021

@author: jp

Implements the TPG 261 Class for experiment monitoring.
"""

from __future__ import annotations

import serial  # type: ignore[import-untyped]

from expmonitor.classes.sensor import Sensor


class TPG261(Sensor):
    """Pfeiffer TPG 261 vacuum gauge sensor implementation."""

    baudrate: int
    timeout: int
    port: str

    def __init__(self, descr: str, port: str) -> None:
        # General sensor setup:
        self.type = "Vacuum Gauge"
        self.descr = descr.replace(" ", "_").lower() + "_vac"  # Multi-word
        self.unit = "mbar"
        self.conversion_fctn = lambda p: float(str(p).split(",")[1])
        super().__init__(self.type, self.descr, self.unit, self.conversion_fctn)
        # TPG261-specific setup:
        self.baudrate = 9600
        self.timeout = 1
        self.port = port

    def connect(self) -> None:
        """Not needed, handled by context manager in self.rcv_vals()."""
        pass

    def disconnect(self) -> None:
        """Not needed, handled by context manager in self.rcv_vals()."""
        pass

    def rcv_vals(self) -> bytes:
        # Receive pressure value as bytes:
        with serial.Serial(
            self.port, baudrate=self.baudrate, timeout=self.timeout
        ) as ser:
            serial_rcv: bytes = ser.readline()
        return serial_rcv


# Execution:
if __name__ == "__main__":
    from expmonitor.config import *  # noqa: F401, F403

    TPG261.test_execution()
