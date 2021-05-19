from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.Devices.TemperatureSensor import *
import multiprocessing


class Phidget:

    def __init__(self, obj_dict):

        for k, v in obj_dict.items():
            setattr(self, k, v)

        if self.phidget_type == 'Thermocouple':
            self.ts_handle = TemperatureSensor()
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

obj_dicts = []

tc1 = {'phidget_type': 'Thermocouple', 'hub_port': 4, 'hub_serial': 561242, 'hub_channel': 0, 'measurement_descr': 'Source'}
obj_dicts.append(tc1)
tc2 = {'phidget_type': 'Thermocouple', 'hub_port': 4, 'hub_serial': 561242, 'hub_channel': 1, 'measurement_descr': 'A/C'}
obj_dicts.append(tc2)
tc3 = {'phidget_type': 'Thermocouple', 'hub_port': 4, 'hub_serial': 561242, 'hub_channel': 2, 'measurement_descr': 'Lab'}
obj_dicts.append(tc3)

def multiproc_fctn(obj_dict):
    tc = Phidget(obj_dict)
    tc.measure()



with multiprocessing.Pool() as pool:
    pool.map(multiproc_fctn, obj_dicts)
