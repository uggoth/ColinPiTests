module_name = 'test_10_D_vl53l5cx_and_hc-sr04_v02.py'
print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
import time
import pigpio
from vl53l5cx.vl53l5cx import VL53L5CX

gpio = pigpio.pi()
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance
driver = VL53L5CX()

alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")

print("Initialising...")
t = time.time()
driver.init()
print(f"Initialised ({time.time() - t:.1f}s)")
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(20)
# Ranging:
driver.start_ranging()

interval = 10
bad_statuses = 0
pre_not_readys = 0
post_not_readys = 0
pre = True
for i in range(90):
    time.sleep(0.05)
    mmus = my_front_ultrasonic.read_mms()
    if (driver.check_data_ready()):
        ranging_data = driver.get_ranging_data()
        st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
        if not (st03 == 5):
            bad_statuses += 1
            continue
        mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
        mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
        mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
        mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
        pre = False
    else:
        if pre:
            pre_not_readys += 1
        else:
            post_not_readys += 1
        continue
    if i%interval == 0:
        rear_distance = (mm15 + mm11) / 2.0
        front_distance = (mm07 + mm03) / 2.0
        margin = 5
        if rear_distance > (front_distance + margin):
            angle = 'CLOSING'
        elif front_distance > (rear_distance + margin):
            angle = 'OPENING'
        else:
            angle = 'ANGLE_OK'
        print ('mm15:{:3} mm11:{:3} mm07:{:3}  mm03:{:3}'.format(
            mm15, mm11, mm07, mm03), angle)

print ('bad_statuses',bad_statuses)
print ('pre_not_readys',pre_not_readys)
print ('post_not_readys',post_not_readys)
my_ultrasonics.close()
