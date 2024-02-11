#  Test command stream handshake
#  Run in conjunction with test_15_A_handshake on the Pico

module_name = 'test_15_A_handshake_IRQ.py'
print (module_name, 'starting')

import time
start_time = time.time()
import pigpio

def callback_up(gpio_pin, level, tick):
    print (' UP ', gpio_pin, level, tick)

def callback_down(gpio_pin, level, tick):
    print ('DOWN', gpio_pin, level, tick)

handshake_pin = 4
gpio = pigpio.pi()
gpio.set_pull_up_down(handshake_pin, pigpio.PUD_UP)

my_callback_up = gpio.callback(handshake_pin, pigpio.RISING_EDGE, callback_up)
my_callback_down = gpio.callback(handshake_pin, pigpio.FALLING_EDGE, callback_down)
time.sleep(60)

gpio.stop()
print (module_name, 'finished')
