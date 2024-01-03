module_name = 'test_00_A_digital_outputs_raw_v01.py'
module_description = 'Testing LEDs and buzzers without using objects'
created_at = '202304301001'

from importlib.machinery import SourceFileLoader
colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
buzzers = my_data.params['BUZZER']
leds = my_data.params['LED']

import pigpio
gpio = pigpio.pi()
import time

def oscillate(frequency, duration):
    delay = 1.0 / float(frequency)
    loops = int(duration / delay)
    for i in range(loops):
        for pin_no in pin_nos:
            gpio.write(pin_no,1)
        time.sleep(delay)
        for pin_no in pin_nos:
            gpio.write(pin_no,0)
        time.sleep(delay)

print (module_name,'starting')

if len(buzzers) > 0:
    for pin_no in buzzers:
        gpio.set_mode(pin_no, pigpio.OUTPUT)
    oscillate(244,2.0)
else:
    print ('no buzzers')

if len(leds) > 0:
    for pin_no in leds:
        gpio.set_mode(pin_no, pigpio.OUTPUT)
    oscillate(4,2.0)
else:
    print ('no LEDs')

gpio.stop()
print (module_name,'finished')
