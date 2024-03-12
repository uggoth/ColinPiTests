module_name = 'test_15_J_joysticks_v03.py'
print (module_name,'starting')
print ('expects test_15_J to be running on the Pico')

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
base_servo = zombie_arm.base_servo
gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
wrist_down = 70
wrist_up = 50
wrist_park = -40
wrist_servo.move_to_and_wait(wrist_up)
base_park = 27
base_servo.move_to_and_wait(base_park)

if my_pico.valid:
    i = 0
    while True:
        time.sleep(0.01)
        serial_no = '{:04}'.format(i)
        command = 'JOYS'
        serial_no, feedback, data = my_pico.do_command(serial_no, command)
        if feedback == 'OKOK':
            if ((command == 'JOYS') and ('NONE' not in data)):
                wrist_joystick = int(data[8:12])
                if wrist_joystick < 0:
                    wrist_pos = wrist_down
                elif wrist_joystick < 25:
                    wrist_pos = wrist_up
                else:
                    wrist_pos = wrist_park
                wrist_servo.move_to_and_wait(wrist_pos)
                switch_pos = int(data[16:20])
                if switch_pos < 0:
                    print ('Exiting on switch 5')
                    my_pico.do_command(serial_no, 'EXIT')
                    break
        else:
            print ('Flushing dodgy feedback')
            got = my_pico.get()
            while got:
                print (got)
                got = my_pico.get()
        i += 1
else:
    print ('*** No Pico')
my_pico.close()
print (module_name, 'finished')
