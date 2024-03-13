module_name = 'test_10_B_vl53l5cx_v01.py'
print (module_name, 'starting')

import time
import pigpio
from vl53l5cx.vl53l5cx import VL53L5CX

gpio = pigpio.pi()
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)
driver = VL53L5CX()

alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")

print("Initialising...")
t = time.time()
driver.init()
print(f"Initialised ({time.time() - t:.1f}s)")
print ('Press the blue button to take a reading')
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(20)
# Ranging:
driver.start_ranging()

previous_time = 0
no_loops = 60
no_zones = 16
interval = 1000  #  milliseconds
for i in range(no_loops):
    time.sleep(interval / 1000.0)
    if ((driver.check_data_ready() and (gpio.read(blue_button) == 0))):
        ranging_data = driver.get_ranging_data()
        now = time.time()
        if previous_time != 0:
            time_to_get_new_data = now - previous_time
            print(f"Print data no : {driver.streamcount: >3d} ({time_to_get_new_data * 1000:.1f}ms)")
        else:
            print(f"Print data no : {driver.streamcount: >3d}")

        for j in range(no_zones):
            print(f"Zone : {j: >3d}, "
                  f"Status : {ranging_data.target_status[driver.nb_target_per_zone * j]: >3d}, "
                  f"Distance : {ranging_data.distance_mm[driver.nb_target_per_zone * j]: >4.0f} mm")
        for j in (12,13,14,15):
            outstring = ''
            for k in range(4):
                l = j - (k*4)
                mm = int(ranging_data.distance_mm[driver.nb_target_per_zone * l])
                outstring += '{:2}:{:4}  '.format(l,mm)
            print (outstring)

        print("")

        previous_time = now

    time.sleep(0.005)

