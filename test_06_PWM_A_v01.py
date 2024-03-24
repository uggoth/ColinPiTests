module_prefix = 'test_06_PWM_A'
module_version = '01'
module_name = module_prefix + '_v' + module_version + '.py'
print (module_name, 'starting')

import pigpio
import time

gpio = pigpio.pi()
servo_pin_no = 19
frequency = 50
gpio.set_PWM_frequency(servo_pin_no, frequency)
gpio.set_PWM_range(servo_pin_no, 20000)
gpio.hardware_PWM(servo_pin_no, 50, 2000)

for i in range(2):
    gpio.set_servo_pulsewidth(servo_pin_no, 1000)
    time.sleep(1)
    gpio.set_servo_pulsewidth(servo_pin_no, 2000)
    time.sleep(1)
    gpio.set_servo_pulsewidth(servo_pin_no, 1500)
    time.sleep(1)
    
gpio.set_servo_pulsewidth(servo_pin_no, 0)
