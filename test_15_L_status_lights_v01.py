module_name = 'test_15_L_status_lights_v01.py'
print (module_name,'starting')
print ('expects main_a_s_a_d to be running on the Pico')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ColObjectsVersion = data_values['ColObjects']
col_objects_name = '/home/pi/ColinPiClasses/' + ColObjectsVersion + '.py'
ColObjects = SourceFileLoader('ColObjects', col_objects_name).load_module()
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py').load_module()
import time
import pigpio
gpio = pigpio.pi()
handshake = CommandStream.Handshake('picoa hs', 4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
if not my_pico.valid:
    print ('*** NO PICO')
    sys.exit(1)
time.sleep(3)
commands = ['SGRN', 'SRED', 'SBLU', 'SOFF']
serial_no = 0
for command in commands:
    serial_no += 1
    serial_no_string = '{:4}'.format(serial_no)
    print (serial_no_string, command)
    my_pico.send_command(serial_no_string, command)
    time.sleep(1)
    
