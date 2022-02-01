#!/usr/bin/bash
# Shell script to set up the RaspberryPi server for experiment monitoring.

echo "Installing ..."
# Set system time for InfluxDB time stamps:
timedatectl set-timezone Europe/Paris
# Make sure everything is up-to-date:
apt update && sudo apt -y upgrade
# To enable X11 forwarding, install the X_Windows package:
apt install xorg
# Set the DISPLAY parameter manually:
export DISPLAY=localhost:10.0
echo "Done."