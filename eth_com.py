 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 08 10:22:13 2019

@author: jp

Module for ethernet communication from PC to Arduino via Ethernet Shield

"""


def dac_output(channel, voltage, output):

    import socket
    import struct
    
    # IP_adr_lockbox = '192.168.1.29'    
    # IP_adr_lockbox = '172.20.217.135'
    IP_adr_lockbox = '172.20.217.9'
    # IP_adr_lockbox = '10.117.53.45'    
    

        
    arduino_port = 6574
        
    # msg_channel = struct.pack('B',channel)
    
    # msg_voltage = struct.pack('H',voltage)
    
    # msg_output = struct.pack('?',output)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.connect((IP_adr_lockbox, arduino_port))
    
    print("Connected.")
    
    s.sendall(b'Hello, world')
    
    msg = s.recv(1024)

    # s.sendall(msg_voltage)
    
    # s.sendall(msg_output)
    
    print(msg)
    
    return msg

if __name__ == '__main__':
    
    msg = dac_output(1, 4095, output=False)