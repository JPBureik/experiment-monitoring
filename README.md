# Experiment Monitoring Software

A software package for automated monitoring of lab equipment, including time series visualization and automatic alerts.

## Architecture

A central server gathers data from different sources, writes them into a database, hosts a graphic interface for visualization and sends automatic alerts based on user-defined criteria.

## Currently supported interfaces

  * Serial
  * TCP/IP
  * Analog (via ADC on Arduino Due)

## Setup

  * Hardware requirements & server setup: See `server_setup.md`.
  * Working with existing interfaces:
    - `config.py` is all you need to modify.
  * Adding your own interfaces:
    - Write a child class to inherit from `sensor.py` to drive your sensor/equipment and interface it with `config.py`.

## Guide to the repository structure:

  * `arduino_exp_monitor`: Contains script to run on ADC.
  * `calibrations`: Contains calibration data and scripts for all equipment.
  * `classes`: Contains driver classes for all interfaces.
  * `utilities`: Contains interface-independent functions.
  * `config.py`: Main configuration file.
  * `exec.py`: Main execution file for Linux service.
