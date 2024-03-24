module_prefix = 'test_10_E_vl53l5cx_straighten'
module_version = '01'
module_name = module_prefix + '_v' + module_version + '.py'
print (module_name, 'starting')
print ('Position robot, then press blue button')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
pi_version = '/home/pi/ColinThisPi/' + ThisPiVersion + '.py'
ThisPi = SourceFileLoader('ThisPi', pi_version).load_module()
import sys
from vl53l5cx.vl53l5cx import VL53L5CX
driver = VL53L5CX()
command_stream_version = '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py'
print (command_stream_version)
CommandStream = SourceFileLoader('CommandStream', command_stream_version).load_module()
import time
import pigpio
gpio = pigpio.pi()
pico_id = 'PICOA'
handshake = CommandStream.Handshake(4, gpio)
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance
for i in range(4):
    mmus = my_front_ultrasonic.read_mms()
    time.sleep(0.1)
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)

alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")

def check_straight():
    global driver
    max_checks = 99
    i = 0
    while i < max_checks:
        i += 1
        if driver.check_data_ready():
            break
        time.sleep(0.01)
    if i >= max_checks:
        return False, -1
    ranging_data = driver.get_ranging_data()
    st15 = ranging_data.target_status[driver.nb_target_per_zone * 15]
    st11 = ranging_data.target_status[driver.nb_target_per_zone * 11]
    st07 = ranging_data.target_status[driver.nb_target_per_zone * 7]
    st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
    if not ((st15 == 5) and (st15 == 5) and (st15 == 5) and (st15 == 5)):
        return False, 0.0
    mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
    mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
    mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
    mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
    print ('mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}'.format(mm15,mm11,mm07,mm03))
    left = (mm15+mm11)/2
    right = (mm07+mm03)/2
    diff = left-right
    return True, diff

print("Initialising...")
t = time.time()
driver.init()
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(40)
driver.start_ranging()
print(f"Initialised ({time.time() - t:.1f}s)")

big_diff = 20
small_diff = 5
ok_diff = 1.5
################################## should learn this
carpet = True
if carpet:
    big_turn = 50
    small_turn = 20
else:
    big_turn = 40
    small_turn = 10
##################################
active_turn = big_turn
while True:
    no_loops = 10000
    flash_loops = 10
    flip_flop = False
    interval = 0.01
    i = 0
    print ('Now waiting for blue button')
    while i < no_loops:
        time.sleep(interval)
        if gpio.read(blue_button) == 0:
            break
        if i%flash_loops == 0:
            flip_flop = not flip_flop
            if flip_flop:
                my_pico.send_command('0000', 'RLC+')
            else:
                my_pico.send_command('0000', 'RLC-')
        i += 1
                
    if i >= no_loops:
        print ('Blue button not pressed. Exiting')
        sys.exit(1)
    wait_time = int(i * interval)
    print ('Blue button pressed after', wait_time, 'seconds . Starting ...')
    time.sleep(0.5)
    max_turns = 15
    turn = 0
    while turn < max_turns:
        success, diff = check_straight()
        adiff = abs(diff)
        if adiff < ok_diff:
            print ('diff OK', diff)
            break
        elif adiff < small_diff:
            active_turn = small_turn
            print ('diff small', diff)
        elif adiff < big_diff:
            active_turn = big_turn
            print ('diff big', diff)
        else:
            active_turn = big_turn
            print ('diff huge', diff)
        turn_amount = '{:04}'.format(active_turn)

        if diff < 0:
            command = 'TRNL' + turn_amount
        else:
            command = 'TRNR' + turn_amount
        print (command)
        my_pico.send_command_and_wait('0000', command)
        time.sleep(0.2)
        turn += 1
    if turn < max_turns:
        print ('straighten OK')
    else:
        print ('**** Failed to correct within',max_turns,'turns')
    mmus = my_front_ultrasonic.read_mms()
    print ('Ultrasonic', mmus)
