#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:50:14 2021

@author: jp

Implements the TPG 300 Class for experiment monitoring.
"""

from __future__ import annotations

from expmonitor.calibrations.calib import Calibrator
from expmonitor.classes.adc.arduino_adc import ArduinoADC
from expmonitor.classes.sensor import Sensor


class TPG300(Sensor):
    """Pfeiffer TPG 300 vacuum gauge sensor with Arduino ADC readout."""

    _calib: Calibrator
    arduino_adc: ArduinoADC
    arduino_channel: int

    def __init__(self, descr: str, adc_analog_in: int) -> None:
        # General sensor setup:
        self.type = "Vacuum Gauge"
        self.descr = descr.replace(" ", "_").lower() + "_vac"  # Multi-word
        self.unit = "mbar"
        self._calib = Calibrator()
        self.conversion_fctn = self._calib.calib_fctn
        super().__init__(
            self.type, self.descr, self.unit, self.conversion_fctn, num_prec=12
        )
        # TPG261-specific setup:
        self.arduino_adc = ArduinoADC()
        self.arduino_channel = adc_analog_in

    def connect(self) -> None:
        """Open the connection to the Arduino."""
        self.arduino_adc.connect()

    def disconnect(self) -> None:
        """Close the connection to the Arduino."""
        self.arduino_adc.disconnect()

    def rcv_vals(self) -> float | None:
        """Receive and return measurement values from Arduino."""
        return self.arduino_adc.measure()[self.arduino_channel]


# Execution:
if __name__ == "__main__":
    from expmonitor.config import *  # noqa: F401, F403

    TPG300.test_execution()
