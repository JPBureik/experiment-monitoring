#!/usr/bin/bash

# Shell script to set up the RaspberryPi server for experiment monitoring.


echo "
Specify a name for the InfluxDB database:
"
read database_name


echo "Setting up server ..."


echo "
--------------------
1/6 Server setup
--------------------
"


# Set the locales corresponding to your region and languages:
rm /etc/locale.gen
cp /mnt/code/experiment-monitoring/server_setup/files/locale.gen /etc/locale.gen
locale-gen
# Set system time for InfluxDB time stamps:
timedatectl set-timezone Europe/Paris

# Make sure everything is up-to-date:
apt update && sudo apt -y upgrade

# To enable X11 forwarding, install the X_Windows package:
apt install xorg

# Set the DISPLAY parameter manually:
export DISPLAY=localhost:10.0


echo "
--------------------
2/6 Installing InfluxDB and Grafana
--------------------
"


# Install InfluxDB:
curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
echo "deb https://repos.influxdata.com/ubuntu bionic stable" | tee /etc/apt/sources.list.d/influxdb.list
apt update
apt install influxdb

# Change the default save location for InfluxDB data:
mkdir /mnt/data/influxdb
sudo chown -R influxdb:influxdb /mnt/data/influxdb
sed -z -i -e 's/\[meta]\n  # Where the metadata\/raft database is stored\n  dir = \"\/var\/lib\/influxdb\/meta\"/\[meta]\n  # Where the metadata\/raft database is stored\n  dir = \"\/mnt\/data\/influxdb\/meta\"/g' /etc/influxdb/influxdb.conf
sed -z -i -e 's/\[data]\n  # The directory where the TSM storage engine stores TSM files.\n  dir = \"\/var\/lib\/influxdb\/data\"\n\n  # The directory where the TSM storage engine stores WAL files.\n  wal-dir = \"\/var\/lib\/influxdb\/wal\"/\[data]\n  # The directory where the TSM storage engine stores TSM files.\n  dir = \"\/mnt\/data\/influxdb\/data\"\n\n  # The directory where the TSM storage engine stores WAL files.\n  wal-dir = \"\/mnt\/data\/influxdb\/wal\"/g' /etc/influxdb/influxdb.conf

# Start the InfluxDB Daemon:
systemctl start influxdb

# Install Grafana:
wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list
apt-get update
apt-get install -y grafana

# Replace the Grafana configuration file:
rm /etc/grafana/grafana.ini
cp ./server_setup/files/grafana.ini /etc/grafana/

# Enable and start the Grafana server:
/bin/systemctl enable grafana-server
/bin/systemctl start grafana-server

# Start Grafana automatically after reboot:
echo "sudo service grafana-server restart" >> /etc/rc.local


echo "
--------------------
3/6 Installing Python and dependencies
--------------------
"


# Install Python 3:
apt install python3-pip

# Install dependencies:
apt-get install libatlas-base-dev libopenjp2-7 libtiff5 python-dev


echo "
--------------------
4/6 Installing the Experiment Monitoring package
--------------------
"


# Install package:
cd /mnt/code/experiment-monitoring
/usr/bin/python3 -m pip install -e .


echo "
--------------------
5/6 Installing drivers for Phidgets
--------------------
"


# Install Phidgets drivers:
cd /tmp
wget https://www.phidgets.com/downloads/phidget22/libraries/linux/libphidget22.tar.gz
tar zxvf libphidget22.tar.gz
rm *.gz
cd "$(ls|grep "libphidget22")"
./configure
make
make install

# Add /usr/local/lib to the system-wide library path:
echo /usr/local/lib >> /etc/ld.so.conf && sudo ldconfig

# Extend the USB access rules:
usermod -a -G dialout $USER
cp plat/linux/udev/99-libphidget22.rules /etc/udev/rules.d
udevadm control --reload


echo "
--------------------
6/7 Setting up the InfluxDB databse:
--------------------
"

# Create the InfluxDB database using the specified database name:
influx -execute 'CREATE DATABASE '$database_name''
# Add the database name to the Experiment Monitoring configuration:
sed -i -e 's/"""mydatabase"""/"'$database_name'"/g' /mnt/code/experiment-monitoring/src/expmonitor/utilities/database.py


echo "
--------------------
7/7 Setting up the Linux service:
--------------------
"


cp /mnt/code/experiment-monitoring/server_setup/files/expmonitor.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/expmonitor.service
sudo chmod +x /mnt/code/experiment-monitoring/expmonitor/exec.py
sudo systemctl daemon-reload


echo "Done."
echo "Rebooting now... "
sudo reboot


[meta]\n  # Where the metadata/raft database is stored
  dir = "/mnt/data/influxdb/meta"



