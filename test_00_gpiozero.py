from gpiozero import LED
import time
led = LED(6)
led.on()
time.sleep(1)
led.off()
