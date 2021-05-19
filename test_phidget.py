from Phidget22.Devices import TemperatureSensor


class Phidget:

    def __init__(self, phidget_type, hub_port, hub_serial, hub_channel, measurement_descr):

        self.phidget_type = phidget_type
        self.hub_port = hub_port
        self.hub_serial = hub_serial
        self.hub_channel = hub_channel
        self.measurement_descr = measurement_descr

        if self.phidget_type == 'Thermocouple':
            self.ts_handle = TemperatureSensor.TemperatureSensor()
            # Set addressing parameters to specify which channel to open:
            self.ts_handle.setHubPort(self.hub_port)
            self.ts_handle.setDeviceSerialNumber(self.hub_serial)
            self.ts_handle.setChannel(self.hub_channel)

    def measure(self):

        # Open your Phidgets and wait for attachment:
        self.ts_handle.openWaitForAttachment(1000)

        temp = self.ts_handle.getTemperature()

        print(self.measurement_descr + ' Temperature: ' + str(temp) + ' °C')

        # Close your Phidgets once the program is done:
        self.ts_handle.close()

all_phidgets = []

tc1 = Phidget('Thermocouple', 4, 561242, 0, 'Source')
all_phidgets.append(tc1)
tc2 = Phidget('Thermocouple', 4, 561242, 1, 'A/C')
all_phidgets.append(tc2)
tc3 = Phidget('Thermocouple', 4, 561242, 2, 'Lab')
all_phidgets.append(tc3)


for phidget in all_phidgets:
    phidget.measure()
