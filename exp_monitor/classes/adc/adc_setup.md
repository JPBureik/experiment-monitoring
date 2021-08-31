# Arduino Analog-to-Digital Converter Setup

## Recommended Hardware
  * [Arduino Due](https://store.arduino.cc/arduino-due)
  * [Arduino Ethernet Shield 2](https://store.arduino.cc/arduino-ethernet-shield-2)
  * [5V Power Supply](https://fr.farnell.com/xp-power/vel12us120-eu-ja/adaptateur-ac-dc-12v-1a/dp/2524421)
  * [3.3V Zener Diodes](https://fr.farnell.com/nexperia/bzx79-c3v3/diode-zener-500mw-3-3v/dp/1097229?MER=sy-me-pd-mi-alte)

## Hardware Setup
  * Protect Arduino entries with Zener diodes.

## Software Setup
  * Use the [Arduino IDE](https://www.arduino.cc/en/software) to open the sketch `adc.ino` and to transfer it onto the Arduino.
  * By design, the Arduino reads out all 12 `AnalogIn` entries and sends the data over the network. This means that the sketch does not need to be updated when you add another analog entry. Just make sure to specify the correct entries in `config.py`.
  * The Arduino is its own sensor class that inherits from the abstract class in `sensor.py`. The sub-classes for equipment that is read out over analog via the Arduino calls the Arduino's `measure` method for its own channel.
