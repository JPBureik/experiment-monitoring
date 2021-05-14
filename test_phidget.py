from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def onTemperatureChange(self, temperature):
	print("Temperature: " + str(temperature))

def main():
	#Create your Phidget channels
	temperatureSensor0 = TemperatureSensor()

	#Set addressing parameters to specify which channel to open (if any)
	temperatureSensor0.setHubPort(0)
	temperatureSensor0.setDeviceSerialNumber(561242)

	#Assign any event handlers you need before calling open so that no events are missed.
	temperatureSensor0.setOnTemperatureChangeHandler(onTemperatureChange)

	#Open your Phidgets and wait for attachment
	temperatureSensor0.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.

	time.sleep(5)

	#Close your Phidgets once the program is done.
	temperatureSensor0.close()

main()
