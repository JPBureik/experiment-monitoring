#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:58:50 2020

@author: jp

Unit conversion for experiment monitoring with Arduino.

Takes lab measurement data (analog voltages) in a list, converts each entry
to corresponding unit and returns them as a list of dictionaries to be stored
in a database.
"""

def unit_conv(analog_signals):
    """ Convert measurement data in list of floats from Arduino to corresponding units."""


    """ ---------- USER INPUT: Measurements ---------- """

    # Lab temperature
    lab_temperature = dict()
    lab_temperature['unit'] = '°C'

    # Science Chamber Vacuum
    sc_vac = dict()
    sc_vac['unit'] = 'mbar'

    """ ---------- Conversion ---------- """
    # def T(V): return ((V - 2.616) / (-10.9e-3)) - 50
    def T(V): return (10.888 - (((-10.888)**2 + 4 * 0.00347 * (1777.3 - V * 1e3))**(1/2))) / (2 * (-0.00347)) + 30

    V1 = analog_signals[1]
    lab_temperature['value'] = T(V1)

    def P(V): return 10**(V - 10.5)

    V2 = analog_signals[2]
    sc_vac['value'] = P(V2)

    """ ---------- Value check ---------- """
    if (((V1 >= 0 and V1 <= 3.3) and (V2 >= 0 and V2 <= 3.3)) and ((lab_temperature['value'] >= -50 and lab_temperature['value'] <= 150) and (sc_vac['value'] >= 1e-11 and sc_vac['value'] <= 1e-2))):
        write_to_db = True
    else:
        write_to_db = False

    # List to be written to database:
    output_list = []
    output_list.append(
        {'measurement': 'lab_temperature',
         'value': lab_temperature['value'],
         'unit': lab_temperature['unit']})
    output_list.append(
	{'measurement': 'sc_vac',
	 'value': sc_vac['value'],
	 'unit': sc_vac['unit']}
        )

    return output_list, write_to_db
