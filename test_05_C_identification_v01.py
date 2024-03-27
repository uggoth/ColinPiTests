module_name = 'test_00_A_digital_outputs_raw_v01.py'
module_description = 'Identify stepper pin nos'
created_at = '202403261001'
print (module_name,'starting')

import pigpio
gpio = pigpio.pi()
import time

pins = [12,7,8,19]

for pin in pins:
    gpio.set_mode(pin, pigpio.OUTPUT)

delay = 3.0

for pin in pins:
    print ('pin',pin)
    gpio.write(pin,1)
    time.sleep(delay)
    gpio.write(pin,0)
    time.sleep(delay)

gpio.stop()
print (module_name,'finished')
