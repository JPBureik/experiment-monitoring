from Phidget22.Devices import TemperatureSensor


class Phidget:

    def __init__(self, phidget_type, hub_port, hub_serial, hub_channel, measurement_descr):

        self.phidget_type = phidget_type
        self.hub_port = hub_port
        self.hub_serial = hub_serial
        self.hub_channel = hub_channel
        self.measurement_descr = measurement_descr

        if self.phidget_type == 'Thermocouple':
            self.unit_str = '°C'
            self.ts_handle = TemperatureSensor.TemperatureSensor()
            # Set addressing parameters to specify which channel to open:
            self.ts_handle.setHubPort(self.hub_port)
            self.ts_handle.setDeviceSerialNumber(self.hub_serial)
            self.ts_handle.setChannel(self.hub_channel)

    def measure(self):
        """ Open connection to Phidget, receive measurement and close."""

        # Open Phidgets and wait for attachment:
        self.ts_handle.openWaitForAttachment(1000)

        temp = self.ts_handle.getTemperature()

        # Close Phidgets once the program is done:
        self.ts_handle.close()

        return temp

    def to_dict(self, temp):
        """ Return dict w/ measurement for JSON to store in influxDB."""

        json_dict = {}
        json_dict['measurement'] = self.measurement_descr.lower() + '_temp'
        json_dict['unit'] = self.unit_str
        json_dict['phidget_hub'] = self.hub_port
        json_dict['phidget_serial'] = self.hub_serial
        json_dict['raw'] = temp
        json_dict['value'] = temp

        return json_dict

if __name__ == '__main__':

    all_phidgets = []
    tc1 = Phidget('Thermocouple', 4, 561242, 0, 'Source')
    all_phidgets.append(tc1)
    tc2 = Phidget('Thermocouple', 4, 561242, 1, 'A/C')
    all_phidgets.append(tc2)
    tc3 = Phidget('Thermocouple', 4, 561242, 2, 'Lab')
    all_phidgets.append(tc3)
    tc4 = Phidget('Thermocouple', 4, 561242, 3, 'Water')
    all_phidgets.append(tc4)
    tc5 = Phidget('Thermocouple', 5, 561242, 0, 'Zeeman1')
    all_phidgets.append(tc5)
    tc6 = Phidget('Thermocouple', 5, 561242, 1, 'Zeeman2')
    all_phidgets.append(tc6)

    for phidget in all_phidgets:
        temp = phidget.measure()
        print(phidget.measurement_descr + ' Tempreature: ' + str(temp))
