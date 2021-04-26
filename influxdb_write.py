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
    from eth_com import rcv_meas
    from unit_conv import unit_conv

    # Create timestamp for database:
    now = datetime.utcnow()  # Grafana assumes UTC
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    # Receive measurements from Arduino:
    analog_signals = rcv_meas()

    # Convert:
    conv_measurements = unit_conv(analog_signals)

    # Initialize database client:
    Nport = 8086
    db_name = 'helium2'
    client = InfluxDBClient(host='localhost', port=Nport, database=db_name)

    # Create JSON:
    json_body = []
    for measurement in conv_measurements:
        if measurement['value']:
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
