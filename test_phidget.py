from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def onTemperatureChange(self, temperature):
	print("Temperature [" + str(self.getChannel()) + "]: " + str(temperature))

def main():
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
	temperatureSensor1.setOnTemperatureChangeHandler(onTemperatureChange)
	temperatureSensor2.setOnTemperatureChangeHandler(onTemperatureChange)

	#Open your Phidgets and wait for attachment
	temperatureSensor0.openWaitForAttachment(5000)
	temperatureSensor1.openWaitForAttachment(5000)
	temperatureSensor2.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	temperatureSensor0.close()
	temperatureSensor1.close()
	temperatureSensor2.close()

main()
