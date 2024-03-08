module_name = 'test_15_D_command_stream_v03.py'
print (module_name,'starting')
print ('expects test_15_D to be running on the Pico')

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
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
commands = ['WHOU','GASH','POSN','EXIT']
i = 0
for command in commands:
    i += 1
    serial_no_sent = '{:04}'.format(i)
    print ('Sending ' + serial_no_sent + command)
    serial_no_received, feedback, data = my_pico.do_command(serial_no_sent,command)
    print (serial_no_received, feedback, data)
time.sleep(1)
my_pico.close()
print (module_name, 'finished')
