module_name = 'test_10_C_HC-SR04_v01.py'
print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()

import time
GPIO = ThisPi.GPIO
pigpio = GPIO.pigpio
gpio = pigpio.pi()
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance
for i in range(9):
    time.sleep(1)
    print (my_front_ultrasonic.read_mms())
my_ultrasonics.close()
