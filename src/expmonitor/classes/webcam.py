#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:15:51 2022

@author: jp

Webcam-based sensor for reading values from displays via OCR.
"""

from __future__ import annotations

from expmonitor.classes.sensor import Sensor
from expmonitor.utilities.img_proc import img_proc


class Webcam(Sensor):
    """Generic sensor class for reading values from displays via webcam OCR."""

    savepath: str

    def __init__(
        self,
        descr: str,
        sensor_type: str,
        unit: str,
        savepath: str,
        num_prec: int | None = None,
    ) -> None:
        self.type = sensor_type
        self.descr = descr
        self.unit = unit
        self.conversion_fctn = lambda t: t  # No conversion needed
        super().__init__(
            self.type, self.descr, self.unit, self.conversion_fctn, num_prec=num_prec
        )
        self.savepath = savepath

    def connect(self) -> None:
        pass  # Image is captured externally

    def disconnect(self) -> None:
        pass  # No persistent connection

    def rcv_vals(self) -> float | None:
        return img_proc(self.savepath)


# Execution:
if __name__ == "__main__":
    from expmonitor.config import *  # noqa: F401, F403

    Webcam.test_execution()
