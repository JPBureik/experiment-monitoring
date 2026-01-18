#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 08:53:25 2021

@author: jp

Implements the Eaton UPS Class for experiment monitoring.
"""

# Standard library imports:
from easysnmp import Session  # pip3 install easysnmp

# Local imports:
from expmonitor.classes.sensor import Sensor


class EatonUPS(Sensor):
    def __init__(self, descr, ip):
        # General sensor setup:
        self.type = "Universal Power Supply"
        self.descr = descr.lower()
        self.unit = None
        self.conversion_fctn = lambda x: x  # No conversion needed
        super().__init__(self.type, self.descr, self.unit, self.conversion_fctn)
        # EatonUPS-specific setup:
        self.ip = ip

    def connect(self):
        # Create SNMP session to be used for all requests:
        self.session = Session(
            hostname=self.ip, security_username="exp_monitor", version=3
        )

    def disconnect(self):
        # Not needed.
        pass

    def rcv_vals(self):
        # Retrieve individual OIDs:
        minutes_rem = int(
            self.session.get(("UPS-MIB::upsEstimatedMinutesRemaining", 0)).value
        )  # min
        charge_rem = int(
            self.session.get(("UPS-MIB::upsEstimatedChargeRemaining", 0)).value
        )  # %
        seconds_on_battery = int(
            self.session.get(("UPS-MIB::upsSecondsOnBattery", 0)).value
        )  # s
        p_out = int(self.session.get(("UPS-MIB::upsOutputPower", 1)).value)  # W
        p_out_max = int(
            self.session.get(("UPS-MIB::upsConfigOutputPower", 0)).value
        )  # W
        load = int(p_out / p_out_max * 100)  # %
        return {
            "Rem-Minutes": {"value": minutes_rem, "unit": "min"},
            "Rem-Charge": {"value": charge_rem, "unit": "%"},
            "On-time": {"value": seconds_on_battery, "unit": "s"},
            "Load": {"value": load, "unit": "%"},
        }

    def measure(self, verbose=False, show_raw=False):
        """Operator overloading for Sensor ABC to handle dict as meas obj."""
        self.connect()
        self.meas_dict = self.rcv_vals()
        for item in self.meas_dict.items():
            # TODO: SPIKE FILTER
            # TODO: CHECK SAVE RAW DATA
            if verbose:
                print(item)
        self.disconnect()

    def to_db(self):
        """Operator overloading for Sensor ABC to handle dict as meas obj."""
        for item in self.meas_dict.items():
            self._db.write(
                (self.descr + " " + item[0]).lower().replace(" ", "_"),
                item[1]["unit"],
                item[1]["value"],
            )
