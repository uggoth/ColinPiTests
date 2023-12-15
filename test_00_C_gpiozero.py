module_name = 'test_00_C_gpiozero.py'
print (module_name, 'starting')
from gpiozero import LED
import time
led = LED(6)
led.on()
time.sleep(1)
led.off()
print (module_name, 'finished')
