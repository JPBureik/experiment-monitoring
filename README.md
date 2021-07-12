# Experiment Monitoring Software

A software package for automated monitoring of lab equipment, including time series visualization and automatic alerts.

## Architecture

A central server gathers data from different sources, writes them into a database, hosts a graphic interface for visualization and sends automatic alerts based on user-defined criteria.

## Currently supported interfaces

  * Serial
  * TCP/IP
  * Analog (via ADC on Arduino Due)

## Setup

  * Hardware requirements & preparing the server: See `server_setup.md`.
  * Working with existing interfaces:
    - `config.py` is all you need to modify.
  * Adding your own interfaces:
    - Write a class to drive your sensor/equipment and interface it with `config.py`.

## Guide to the individual modules:

  * `config.py`: Main configuration file.
  * ...
