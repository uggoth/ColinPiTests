module_name = 'test_15_G_various_commands_v04.py'
print (module_name,'starting')
print ('expects test_15_G to be running on the Pico')

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
handshake = CommandStream.Handshake('picoa hs', 4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

#  DRIVE format is DRIVssssttttddddcccc where:
#  ssss is steering value from -100 (hard left) to +100 (hard right)
#  tttt is throttle value from -100 (hard reverse) to +100 (full speed ahead)
#  dddd is optional duration in milliseconds. If zero or not present do until told to stop
#  cccc is an optional crab value from -100 (left) to +100 (right) (mecanum only)

command_set = 1

if my_pico.valid:
    if command_set == 1:
        commands = ['DRIV   0  70 500',
                    'DRIV   0   0 300',
                    'DRIV   0 -70 500',
                    'DRIV   0   0 300',
                    'DRIV  50   0 900',
                    'DRIV   0   0 300',
                    'DRIV -50   0 900']
    elif command_set == 2:
        commands = ['SRED',
                    'WAIT2000',
                    'SGRN',
                    'WAIT2000',
                    'SBLU',
                    'WAIT2000',
                    'SRED',
                    'WAIT2000',
                    'SOFF']
    i = 0
    for command in commands:
        serial_no = '{:04}'.format(i)
        print (' ')
        print (serial_no, command)
        print (my_pico.send_command(serial_no, command))
        i += 1
        time.sleep(2)
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
