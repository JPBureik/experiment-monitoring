#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:36:28 2020

@author: jp

Python interface for influDB databases.

Takes a list of floats or ints and writes them into a specified influxDB
database.
"""


def influxdb_write():
    """ Receive measurement data, convert and write into influxDB."""

    # Standard library imports:
    from influxdb import InfluxDBClient
    from datetime import datetime

    # Local imports:
    from inbounds_check import bounds, is_inbounds
    from eth_com import rcv_meas
    from unit_conv import unit_conv
    from phidget import Phidget
    from serial_com import tpg261_meas

    # Create timestamp for database:
    now = datetime.utcnow()  # Grafana assumes UTC
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    # Receive measurements from Arduino:
    analog_signals = rcv_meas()

    # Convert:
    conv_measurements = unit_conv(analog_signals)

    # Phidgets:
    all_phidgets = []
    tc1 = Phidget('Thermocouple', 4, 561242, 0, 'Source')
    all_phidgets.append(tc1)
    tc2 = Phidget('Thermocouple', 4, 561242, 1, 'A/C')
    all_phidgets.append(tc2)
    tc3 = Phidget('Thermocouple', 4, 561242, 2, 'Lab')
    all_phidgets.append(tc3)

    for phidget in all_phidgets:
        temp = phidget.measure()
        json_dict = phidget.to_dict(temp)
        conv_measurements.append(json_dict)

    # Serial communication:
    primary_vac = tpg261_meas('/dev/ttyUSB0')
    conv_measurements.append(primary_vac)

    # Initialize database client:
    Nport = 8086
    db_name = 'helium2'
    client = InfluxDBClient(host='localhost', port=Nport, database=db_name)

    # Check bounds and create JSON:
    json_body = []
    for measurement in conv_measurements:
        if measurement['value']:
            if is_inbounds(
                    measurement['value'],
                    bounds[measurement['measurement']]['lower'],
                    bounds[measurement['measurement']]['upper']
                    ):
                json_body.append(
                    {
                        "measurement": measurement['measurement'],
                        "tags": {
                            "unit": measurement['unit'],
                        },
                        "time": dt_string,
                        "fields": {
                            "value": measurement['value'],
                            "raw": measurement['raw'],
                        }
                    }
                )

    # Write to database:
    client.write_points(json_body)


if __name__ == '__main__':

    influxdb_write()
