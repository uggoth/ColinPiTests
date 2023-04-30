module_name = 'test_00_A_digital_outputs_raw_v01.py'
created_at = '202304301001'

import pigpio
gpio = pigpio.pi()
import time

print (module_name,'starting')

pin_nos = [6,13,19,26]
for pin_no in pin_nos:
    gpio.set_mode(pin_no, pigpio.OUTPUT)

frequency = 1000
duration = 2.0
delay = 1.0 / float(frequency)
loops = int(duration / delay)

print ('timed loop')
for i in range(loops):
    for pin_no in pin_nos:
        gpio.write(pin_no,1)
    time.sleep(delay)
    for pin_no in pin_nos:
        gpio.write(pin_no,0)
    time.sleep(delay)

gpio.stop()
print (module_name,'finished')
