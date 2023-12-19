module_name = 'test_00_C_gpiozero.py'
print (module_name, 'starting')
##### attach LED to GPIO 6 ############################
from gpiozero import LED
import time
led = LED(6)
for i in range(9):
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
print (module_name, 'finished')
