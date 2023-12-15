module_name = 'test_01_A_digital_input_object_v03.py'
print (module_name, "starting")
print ("")

import GPIOPi_v45 as GPIO
import time


pin_no = 4
pin_name = 'Red Button'
test_pin = GPIO.Switch(pin_name, pin_no)

for i in range(20):
    print (test_pin.get())
    time.sleep(1)

print ("")
print (module_name, "finished")
