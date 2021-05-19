from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.TemperatureSensor import *
import traceback
import time


class Phidget:

    def __init__(self, phidget_type, hub_idx, hub_serial, hub_channel, measurement_descr):

        self.phidget_type = phidget_type
        self.hub_idx = hub_idx
        self.hub_serial = hub_serial
        self.hub_channel = hub_channel
        self.measurement_descr = measurement_descr

    def onTemperatureChange(self, temperature):
        print(channel_id[self.getChannel()] + " Temperature: " + str(temperature))

    def onError(self, code, description):
    	print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
    	print("Description [" + str(self.getChannel()) + "]: " + str(description))
    	print("----------")

    def measure(self):
        try:
    		Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")
    		#Create your Phidget channels
    		temperatureSensor0 = TemperatureSensor()
    		temperatureSensor1 = TemperatureSensor()
    		temperatureSensor2 = TemperatureSensor()

    		#Set addressing parameters to specify which channel to open (if any)
    		temperatureSensor0.setHubPort(4)
    		temperatureSensor0.setDeviceSerialNumber(561242)
    		temperatureSensor0.setChannel(0)
    		temperatureSensor1.setHubPort(4)
    		temperatureSensor1.setDeviceSerialNumber(561242)
    		temperatureSensor1.setChannel(1)
    		temperatureSensor2.setHubPort(4)
    		temperatureSensor2.setDeviceSerialNumber(561242)
    		temperatureSensor2.setChannel(2)

    		#Assign any event handlers you need before calling open so that no events are missed.
    		temperatureSensor0.setOnTemperatureChangeHandler(onTemperatureChange)
    		temperatureSensor0.setOnErrorHandler(onError)
    		temperatureSensor1.setOnTemperatureChangeHandler(onTemperatureChange)
    		temperatureSensor1.setOnErrorHandler(onError)
    		temperatureSensor2.setOnTemperatureChangeHandler(onTemperatureChange)
    		temperatureSensor2.setOnErrorHandler(onError)

    		#Open your Phidgets and wait for attachment
    		temperatureSensor0.openWaitForAttachment(5000)
    		temperatureSensor1.openWaitForAttachment(5000)
    		temperatureSensor2.openWaitForAttachment(5000)

    		#Do stuff with your Phidgets here or in your event handlers.

    		time.sleep(5)

    		#Close your Phidgets once the program is done.
    		temperatureSensor0.close()
    		temperatureSensor1.close()
    		temperatureSensor2.close()

    	except PhidgetException as ex:
    		#We will catch Phidget Exceptions here, and print the error informaiton.
    		traceback.print_exc()
    		print("")
    		print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

tc1 = Phidget('Thermocouple', 4, 561242, 0, 'Source')
tc2 = Phidget('Thermocouple', 4, 561242, 1, 'A/C')
tc3 = Phidget('Thermocouple', 4, 561242, 2, 'Lab')


for phidget in [tc1, tc2, tc3]:
    phidget.measure()