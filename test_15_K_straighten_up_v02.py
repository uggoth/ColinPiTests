module_name = 'test_15_K_straighten_up_v02.py'
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
import pigpio
gpio = pigpio.pi()
handshake = CommandStream.Handshake('picoa hs', 4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
if not my_pico.valid:
    print ('*** NO PICO')
    sys.exit(1)
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

poll_loops = 1000
flash_interval = 10
flip_flop = False
for i in range(poll_loops):
    time.sleep(0.01)
    if gpio.read(blue_button) == 0:
        break
    if i%flash_interval == 0:
        flip_flop = not flip_flop
        if flip_flop:
            my_pico.send_command('0000', 'SGRN')
        else:
            my_pico.send_command('0000', 'SOFF')
            
if i >= poll_loops:
    print ('Blue button not pressed. Exiting')
    my_pico.send_command('0000', 'SOFF')
    sys.exit(1)
print ('Blue button pressed. Starting ...')
time.sleep(1)

success = False

for i in range(10):
    time.sleep(0.05)
    if driver.check_data_ready():
        ranging_data = driver.get_ranging_data()
        st15 = ranging_data.target_status[driver.nb_target_per_zone * 15]
        st11 = ranging_data.target_status[driver.nb_target_per_zone * 11]
        st07 = ranging_data.target_status[driver.nb_target_per_zone * 7]
        st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
        if not ((st15 == 5) and (st15 == 5) and (st15 == 5) and (st15 == 5)):
            continue
        mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
        mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
        mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
        mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
        measurements = 'mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}'.format(mm15,mm11,mm07,mm03)
        left = (mm15+mm11)/2
        right = (mm07+mm03)/2
        diff = abs(left-right)
        if diff < 5:
            print ('Straight', measurements)
            success = True
            break
        if left < right:
            print ('Turning Left', measurements)
            command = 'TRNL0040'
        else:
            print ('Turning Right', measurements)
            command = 'TRNR0040'
        my_pico.send_command('0000', command)

if success:
    print ('---- Success ----')
else:
    print ('****FAILED ****')

ColObjects.ColObj.close_all()
print (module_name, 'finished')
