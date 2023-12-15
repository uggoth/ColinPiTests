module_name = 'test_00_B_digital_outputs_object_v01.py'
created_at = '202304301001'

import GPIOPi_v43 as GPIO
gpio = GPIO.gpio
import time

print (module_name,'starting')

test_pin = GPIO.DigitalOutput('Test Pin', 'OUTPUT', 6)
frequency = 1000
duration = 2.0
delay = 1.0 / float(frequency)
loops = int(duration / delay)

print ('timed loop')
for i in range(loops):
    test_pin.set('ON')
    time.sleep(delay)
    test_pin.set('OFF')
    time.sleep(delay)

test_pin.close()
gpio.stop()

print (module_name,'finished')
