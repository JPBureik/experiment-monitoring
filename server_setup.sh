#!/usr/bin/bash

# Shell script to set up the RaspberryPi server for experiment monitoring.


echo "Setting up server ..."


# # --------------------
# # 1) Server setup
# # --------------------


# # Set system time for InfluxDB time stamps:
# timedatectl set-timezone Europe/Paris

# # Make sure everything is up-to-date:
# apt update && sudo apt -y upgrade

# # To enable X11 forwarding, install the X_Windows package:
# apt install xorg

# # Set the DISPLAY parameter manually:
# export DISPLAY=localhost:10.0


# # --------------------
# # 2) Installing InfluxDB and Grafana
# # --------------------


# # Install InfluxDB:
# curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
# echo "deb https://repos.influxdata.com/ubuntu bionic stable" | tee /etc/apt/sources.list.d/influxdb.list
# apt update
# apt install influxdb

# # Replace the InfluxDB configuration file:
# rm /etc/influxdb/influxdb.conf
# cp ./server_setup/files/influxdb.conf /etc/influxdb/

# # Start the InfluxDB Daemon:
# systemctl start influxdb

# # Install Grafana:
# wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -
# echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list
# apt-get update
# apt-get install -y grafana

# # Replace the Grafana configuration file:
# rm /etc/grafana/grafana.ini
# cp ./server_setup/files/grafana.ini /etc/grafana/

# # Enable and start the Grafana server:
# /bin/systemctl enable grafana-server
# /bin/systemctl start grafana-server

# # Start Grafana automatically after reboot:
# echo "sudo service grafana-server restart" >> /etc/rc.local


# # --------------------
# # 3) Installing Python and dependencies
# # --------------------


# # Install Python 3:
# apt install python3-pip

# # Install dependencies:
# apt-get install libatlas-base-dev libopenjp2-7 libtiff5 python-dev


# --------------------
# 4) Installing the Experiment Monitoring package
# --------------------


# Create and activate virtual environment:
/usr/bin/python3 -m pip install virtualenv
/usr/bin/python3 -m virtualenv venv
source ./venv/bin/activate

# Install package:
/usr/bin/python3 -m pip install -e .

echo "Done."