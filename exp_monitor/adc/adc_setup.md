# Analog-to-Digital Converter Setup

## Recommended Hardware

  * [Arduino Due](https://store.arduino.cc/arduino-due)
  * [Arduino Ethernet Shield 2](https://store.arduino.cc/arduino-ethernet-shield-2)

## Preparing the Arduino
  * Use the [Arduino IDE](https://www.arduino.cc/en/software) to open the sketch `adc.ino` and to transfer it onto the Arduino.

  * If you want to monitor analog signals that can exceed 3.3 V, it is recommended that you protect the entries of the Arduino with [Zener diodes](https://fr.farnell.com/nexperia/bzx79-c3v3/diode-zener-500mw-3-3v/dp/1097229?MER=sy-me-pd-mi-alte).
  * The Arduino sketch `adc.ino` is designed to work with `eth_com.py` over the local network. Make sure your RaspberryPi server and the Arduino are on the same network and can communicate.
  * By design, the Arduino reads out all 12 `AnalogIn` entries and sends the data over the network. This means that the sketch does not need to be updated when you add another analog entry. Just make sure to specify the correct entries in `config.py`.
