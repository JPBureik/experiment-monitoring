#!/usr/bin/bash

# Shell script to test communication to connected Phidgets.

cd /tmp
wget https://www.phidgets.com/downloads/phidget22/examples/python/Manager/Phidget22_HelloWorld_Python_Ex.zip
unzip Phidget22_HelloWorld_Python_Ex.zip
/usr/bin/python3 HelloWorld.py