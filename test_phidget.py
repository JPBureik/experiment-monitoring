from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.TemperatureSensor import *
import traceback
import time


class Phidget:

    def __init__(self, phidget_type, hub_port, hub_serial, hub_channel, measurement_descr):

        self.phidget_type = phidget_type
        self.hub_port = hub_port
        self.hub_serial = hub_serial
        self.hub_channel = hub_channel
        self.measurement_descr = measurement_descr

        def onError(self, code, description):
        	print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
        	print("Description [" + str(self.getChannel()) + "]: " + str(description))
        	print("----------")

        if self.phidget_type == 'Thermocouple':
            self.ts_handle = TemperatureSensor()
            # Set addressing parameters to specify which channel to open:
            self.ts_handle.setHubPort(self.hub_port)
            self.ts_handle.setDeviceSerialNumber(self.hub_serial)
            self.ts_handle.setChannel(self.hub_channel)
            self.ts_handle.setOnErrorHandler(onError)

    def measure(self):
        try:
            Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")

            # Open your Phidgets and wait for attachment:
            self.ts_handle.openWaitForAttachment(1000)

            temp = self.ts_handle.getTemperature()

            print(self.measurement_descr + ' Temperature: ' + str(temp) + ' °C')

            # Close your Phidgets once the program is done:
            self.ts_handle.close()

        except PhidgetException as ex:
            # Catch Phidget Exceptions and print the error information:
            traceback.print_exc()
            print("")
            print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

tc1 = Phidget('Thermocouple', 4, 561242, 0, 'Source')
tc2 = Phidget('Thermocouple', 4, 561242, 1, 'A/C')
tc3 = Phidget('Thermocouple', 4, 561242, 2, 'Lab')


for phidget in [tc2, tc1, tc3]:
    phidget.measure()