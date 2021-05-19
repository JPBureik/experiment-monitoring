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



Code Samples

API	Detail	Language	OS
TemperatureSensor 	Visual Studio GUI 	C# 	Windows 	Download
VoltageInput 	Visual Studio GUI 	C# 	Windows 	Download
TemperatureSensor 		Java 	Android 	Download
VoltageInput 		Java 	Android 	Download
TemperatureSensor 		JavaScript 	Browser 	Download
VoltageInput 	Multi-Channel Example 	JavaScript 	Browser 	Download
VoltageInput 		JavaScript 	Browser 	Download
TemperatureSensor 		Max/MSP 	Multiple 	Download
VoltageInput 		Max/MSP 	Multiple 	Download
TemperatureSensor 		Objective-C 	macOS 	Download
VoltageInput 		Objective-C 	macOS 	Download
TemperatureSensor 		Swift 	macOS 	Download
TemperatureSensor 		Swift 	iOS 	Download
VoltageInput 		Swift 	macOS 	Download
VoltageInput 		Swift 	iOS 	Download
TemperatureSensor 		Visual Basic .NET 	Windows 	Download
VoltageInput 		Visual Basic .NET 	Windows 	Download
Need help? Call us
+1 403 282-7335

Monday - Friday
8:00am - 4:00pm MDT
Connect with us
Phidgets Inc.

We believe in getting problems solved quickly and projects finished on time. That's why we specialize in making affordable, easy to use sensors and controllers that require minimal electronics knowledge.

    About Us
    Dealers
    Terms and Conditions
    Contact Us

© Phidgets Inc. 2016, Inc. Privacy Policy Terms and Conditions Software Licenses
