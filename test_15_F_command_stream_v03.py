module_name = 'test_15_F_command_stream_v01.py'
print (module_name,'starting')
print ('expects test_15_F to be running on the Pico')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' +
                          ThisPiVersion + '.py').load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' +
                                 data_values['CommandStream'] + '.py').load_module()
import time
import pigpio

gpio = pigpio.pi()
#handshake = CommandStream.Handshake('picor', 4, gpio)
#pico_id = 'PICOR'
handshake = CommandStream.Handshake('picor', 18, gpio)
pico_id = 'LINES'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

if my_pico.valid:
    commands = ['DUMMY','WHOU','DUMMY','MFWD0050',
            'DUMMY','MSTP','DUMMY']
    i = 0
    for command in commands:
        serial_no = '{:04}'.format(i)
        print (' ')
        print (serial_no, command)
        time.sleep(1)
        print (my_pico.send_command(serial_no, command))
        i += 1
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
