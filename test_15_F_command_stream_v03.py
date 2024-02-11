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
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

serial_no = 1
if my_pico.valid:
    msgs = ['DUMMY','WHOU','DUMMY','MFWD0050',
            'DUMMY','MSTP','DUMMY','EXIT']
    for msg in msgs:
        print (' ')
        print (serial_no, msg)
        time.sleep(1)
        sno = '{:04.0f}'.format(serial_no)
        print (my_pico.do_command(sno + msg))
        serial_no += 1
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
