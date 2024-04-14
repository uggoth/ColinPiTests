module_name = 'test_15_M_wall_tracking_v04.py'
print (module_name,'starting')
print ('expects main_autonomous to be running on the Pico')

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
from vl53l5cx.vl53l5cx import VL53L5CX
import time
import sys
import pigpio
gpio = pigpio.pi()
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance

def front_ok(distance=335):
    front_mms = my_front_ultrasonic.read_mms()
    if front_mms < distance:
        return True
    else:
        return False

def get_offsets():
    mmus = my_front_ultrasonic.read_mms()
    max_fails = 5
    for i in range(max_fails):
        if driver.check_data_ready():
            ranging_data = driver.get_ranging_data()
            st15 = ranging_data.target_status[driver.nb_target_per_zone * 15]
            st11 = ranging_data.target_status[driver.nb_target_per_zone * 11]
            st07 = ranging_data.target_status[driver.nb_target_per_zone * 7]
            st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
            if ((st15 == 5) and (st11 == 5) and (st07 == 5) and (st03 == 5)):
                mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
                mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
                mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
                mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
                return True, mm15, mm11, mm07, mm03, mmus
    print ('**** No vl53 ranging data found within ',max_fails,'attempts ****')
    return False, 0.0, 0.0, 0.0, 0.0, 0.0
        
def check_straight():
    success, mm15, mm11, mm07, mm03, mmus = get_offsets
    if success:
        left = (mm15+mm11)/2
        right = (mm07+mm03)/2
        diff = left-right
        print ('diff:{:4}  mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}  mmus:{:4}'.format(
            diff, mm15, mm11, mm07, mm03, mmus))
        return True, diff
    else:
        return False, 0

def straighten_up(attempts):
    success = False
    left_count = 0
    right_count = 0
    for i in range(attempts):
        time.sleep(0.05)
        ok, diff = check_straight()
        if ok:
            if abs(diff) < 4:
                print ('Straight', diff)
                success = True
                break
            if diff < 0:
                command = 'TRNL0030'
                print (command)
                left_count += 1
            else:
                command = 'TRNR0030'
                print (command)
                right_count += 1
            my_pico.send_command('0000', command)
        else:
            print ('No diff')
    if left_count > right_count:
        direction = 'LEFT'
    elif right_count > left_count:
        direction = 'RIGHT'
    else:
        direction = 'NONE'
    return success, direction, left_count, right_count

def next_command(command):
    global serial_no
    serial_no += 1
    serial_no_string = '{:04}'.format(serial_no)
    return my_pico.send_command(serial_no_string, command)
   
def wait_for_blue(blue_button, poll_loops):
    flash_interval = 7
    flip_flop = False
    for i in range(poll_loops):
        time.sleep(0.01)
        if gpio.read(blue_button) == 0:
            return True
        if i%flash_interval == 0:
            flip_flop = not flip_flop
            if flip_flop:
                next_command('SGRN')
            else:
                next_command('SOFF')
    return False

def calc_steering(mm03, mm07, mm11, mm15, previous_offset, previous_angle):
    avg_offset = (mm07 + mm03) / 2
    if avg_offset > 350:
        steering = 0
        stopping = True
        steering_info = 'STOPPING'
        return steering, stopping, steering_info, avg_offset, 'STOPPING'
    if avg_offset < 165:
        offset = 'TOO_CLOSE'
    elif avg_offset > 185:
        offset = 'TOO_FAR'
    else:
        offset = 'DISTANCE_OK'

    margin = 5
    if avg_offset < (previous_offset - margin):
        angle = 'CLOSING'
    elif avg_offset > (previous_offset + margin):
        angle = 'OPENING'
    else:
        angle = 'ANGLE_OK'
        
    steering_info = offset + ' ' + angle + ' ' + previous_angle
    steering_calc = {
        'TOO_CLOSE OPENING OPENING': 0,
        'TOO_CLOSE CLOSING OPENING': 30,
        'TOO_CLOSE ANGLE_OK OPENING': 20,
        'TOO_FAR OPENING OPENING':-30,
        'TOO_FAR CLOSING OPENING':-6,
        'TOO_FAR ANGLE_OK OPENING':-20,
        'DISTANCE_OK OPENING OPENING':-0,
        'DISTANCE_OK CLOSING OPENING':0,
        'DISTANCE_OK ANGLE_OK OPENING':0,

        'TOO_CLOSE OPENING CLOSING': 0,
        'TOO_CLOSE CLOSING CLOSING': 30,
        'TOO_CLOSE ANGLE_OK CLOSING': 10,
        'TOO_FAR OPENING CLOSING':-20,
        'TOO_FAR CLOSING CLOSING':-6,
        'TOO_FAR ANGLE_OK CLOSING':-20,
        'DISTANCE_OK OPENING CLOSING':-6,
        'DISTANCE_OK CLOSING CLOSING':-6,
        'DISTANCE_OK ANGLE_OK CLOSING':0,

        'TOO_CLOSE OPENING ANGLE_OK': 10,
        'TOO_CLOSE CLOSING ANGLE_OK': 40,
        'TOO_CLOSE ANGLE_OK ANGLE_OK': 20,
        'TOO_FAR OPENING ANGLE_OK':-20,
        'TOO_FAR CLOSING ANGLE_OK':-6,
        'TOO_FAR ANGLE_OK ANGLE_OK':-20,
        'DISTANCE_OK OPENING ANGLE_OK':-6,
        'DISTANCE_OK CLOSING ANGLE_OK':-6,
        'DISTANCE_OK ANGLE_OK ANGLE_OK':0
        }

    steering = steering_calc[steering_info]
    return steering, False, steering_info, avg_offset, angle

serial_no = 1

handshake = CommandStream.Handshake('picoa hs', 4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
if not my_pico.valid:
    print ('*** NO PICO')
    sys.exit(1)
next_command('STOP')
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
driver = VL53L5CX()
alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")
print("Initialising...")
t = time.time()
driver.init()
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(40)
driver.start_ranging()
print(f"Initialised ({time.time() - t:.1f}s)")
print ('Now waiting for blue button')
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)

max_not_ready = 100
max_bad_status = 100
no_zones = 16
interval = 300  #  milliseconds
legs = ['TRNR','TRNR','TRNL','TRNL','TRNR','STOP']
leg = 0
not_ready = 0
bad_status = 0
steering = 0
delay = 0

throttle = 40
previous_offset = 0
previous_angle = 'ANGLE_OK'
check_loops = 40

while True:
    if wait_for_blue(blue_button, 500000):
        print ('Blue button pressed. Starting ...')
    else:
        print ('Blue button not pressed. Start again')
        continue
    next_command('SGRN')
    time.sleep(4)
    next_command('SBLU')

    command = 'DRIV{:04}{:04}{:04}'.format(steering, throttle, delay)
    print (next_command(command))

    for i in range(check_loops):
        if gpio.read(blue_button) == 0:
            break
        if not front_ok:
            print ('Hit Front')
            break
        success, mm15, mm11, mm07, mm03, mmus = get_offsets()
        if not success:
            print ('**** no offsets ****')
            break
        steering, stopping, steering_info, avg_offset, angle = calc_steering(
            mm15, mm11, mm07, mm03, previous_offset, previous_angle)
        previous_offset = avg_offset
        previous_angle = angle
        if stopping:
            print ('STOPPING BECAUSE OF LARGE OFFSET', avg_offset)
            break
        abs_steering = abs(steering)
        if abs_steering > 15:
            throttle_m = int(throttle * 0.8)
        elif abs_steering < 5:
            throttle_m = int(throttle * 1.2)
        else:
            throttle_m = throttle
        command = 'DRIV{:4}{:4}{:4}'.format(steering, throttle_m, delay)
        print ('offs:{:3} steer:{:3}'.format(avg_offset, steering), '\n',
               steering_info, command, next_command(command), '\n')
        time.sleep(interval / 1000.0)
    if success and not stopping:
        print ('STOPPING BECAUSE OF LOOP LIMIT')
    command = 'STOP'
    print (next_command(command))

time.sleep(1)
next_command('STOP')

my_ultrasonics.close()
my_pico.close()
handshake.close()
print (module_name, 'finished')
