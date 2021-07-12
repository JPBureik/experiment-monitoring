#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 08 10:22:13 2019

@author: jp

Ethernet communication module for experiment monitoring.

This module reads out all 12 Analog Input signals sent from the Arduino over
TCP/IP and returns them as floats in a list.

The entries of the list correspond to the Analog Inputs in ascending order,
i.e. A0 through A11.

Note that it always returns a list of length 12, regardless of how many Analog
Inputs are used. The unused analog pins will float, so be sure to correctly
identify the signals to be monitored.

"""


def rcv_meas():

    import socket
    IP_adr_arduino = '10.117.53.45'  # Static IP: IOGS network
    # IP_adr_arduino = '172.20.217.9' # DHCP: Visitor network - not recommended

    arduino_port = 6574  # Match to server side port

    buffer_size = 2**12

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IP_adr_arduino, arduino_port))

    s.sendall(b'a')  # Send a non-empty message to initialize TCP/IP com

    # Measurement data: 12-bit int -> receive msg as 2**8 * byte1 + byte2

    analog_signals = {}

    for channel in range(12):

        # Receive both bytes successively:
        byte1 = s.recv(buffer_size)
        byte2 = s.recv(buffer_size)
        # Restore original 12-bit integer:

        reconstr = 2**8*(int.from_bytes(byte1, 'little')) +\
            int.from_bytes(byte2, 'little')

        # Convert to voltage:
        voltage = reconstr / 2**12 * 3.25

        analog_signals[channel] = voltage

    return analog_signals


if __name__ == '__main__':

    analog_signals = rcv_meas()
    print(analog_signals)
