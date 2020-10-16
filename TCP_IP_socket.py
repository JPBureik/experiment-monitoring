#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 14:29:13 2020

@author: jp
"""

import socket
import time

TCP_IP = '172.20.217.9'
TCP_PORT = 23
BUFFER_SIZE = 20
MESSAGE = "Hello, World!"

msg = []

timer = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
print('Connected.')
while timer < 10:
    data = s.recv(BUFFER_SIZE)
    msg.append(data)
    timer += 1
    time.sleep(1)
    print(timer)
s.close()

print("received data:", msg)