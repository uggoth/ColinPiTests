#  Test command stream handshake
#  Run in conjunction with test_15_A... on the Pico

module_name = 'test_15_A2_handshake_obj.py'
print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py').load_module()
import time
import pigpio
gpio = pigpio.pi()
import sys
my_handshake = CommandStream.Handshake(4, gpio)
previous = my_handshake.is_on()
print ('Initial value:', previous)
for i in range(900):
    new = my_handshake.is_on()
    if new != previous:
        print (new)
        previous = new
    time.sleep(0.01)

my_handshake.close()
print (module_name, 'finished')
