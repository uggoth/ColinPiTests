module_name = 'test_10_D_vl53l5cx_and_hc-sr04_v01.py'
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

def check_leg_end():
    mmus = my_front_ultrasonic.read_mms()
    if (driver.check_data_ready()):
        ranging_data = driver.get_ranging_data()
        st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
        if not (st03 == 5):
            print ('dodgy vl53l5cx status')
            return None
        mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
        print ('mm03:{:4}  mmus{:4}  '.format(mm03,mmus))
        if mmus < 150 or mm03 > 300:
            return True
        else:
            return False
    else:
        print ('vl53l5cx not ready')
        return None

for i in range(8):
    time.sleep(3)
    print (check_leg_end())

my_ultrasonics.close()
