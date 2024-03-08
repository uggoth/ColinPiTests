module_name = 'test_15_H_data_v03.py'
print (module_name,'starting')
print ('expects test_15_H to be running on the Pico')

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
zombie_arm = ThisPi.ZombieArm()
wrist_servo = zombie_arm.wrist_servo

gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

if my_pico.valid:
    commands = ['DUMMY','WHOU','JOYS','JOYS','JOYS','JOYS','JOYS','JOYS','JOYS','JOYS','JOYS','JOYS','EXIT']
    i = 0
    for command in commands:
        serial_no = '{:04}'.format(i)
        print (' ')
        print (serial_no, command)
        time.sleep(1)
        serial_no, feedback, data = my_pico.do_command(serial_no, command)
        print (serial_no, feedback, data)
        if feedback == 'OKOK':
            if ((command == 'JOYS') and ('NONE' not in data)):
                wrist_pos = int(data[8:12])
                wrist_servo.move_to_and_wait(wrist_pos)
        else:
            got = my_pico.get()
            while got:
                print (got)
                got = my_pico.get()
        i += 1
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
