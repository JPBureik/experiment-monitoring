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
  * The Arduino is its own sensor class that inherits from the abstract class in `sensor.py`. This is necessary because in order to allow for faster execution cycles of the experiment monitoring system, the analog entries of the Arduino are only read out once per cycle, and not every time a different sensor class calls it `measure` method.
  * Therefore, sensors and equipment that are read out over analog should be subclasses of the Arduino class and use its `super().measure` method.
  * In order for its subclasses to be able to make independent `measure` calls, the analog values of the Arduino are stored locally for the duration of the cycle.
