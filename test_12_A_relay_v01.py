module_prefix = 'test_12_A_relay'
module_version = '01'
module_name = module_prefix + '_v' + module_version + '.py'
print (module_name)

from importlib.machinery import SourceFileLoader
colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
relay_pin_no = my_data.params['ATT3_PIN_NO']

import pigpio
gpio = pigpio.pi()
import time

gpio.set_mode(relay_pin_no, pigpio.OUTPUT)

delay = 2

for i in range(2):
    gpio.write(relay_pin_no,1)
    time.sleep(delay)
    gpio.write(relay_pin_no,0)
    time.sleep(delay)

gpio.stop()
print (module_name,'finished')
