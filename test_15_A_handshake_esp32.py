#  Test command stream handshake
#  Run in conjunction with HandshakeTestA on the ESP32

module_name = 'test_15_A_handshake_esp32.py'
print (module_name, 'starting')

import time
start_time = time.time()
import pigpio

handshake_pin = 18
gpio = pigpio.pi()
gpio.set_pull_up_down(handshake_pin, pigpio.PUD_UP)
previous = gpio.read(handshake_pin)
for i in range(9000):
    new = gpio.read(handshake_pin)
    if new != previous:
        print (new)
        previous = new
    time.sleep(0.01)

gpio.stop()
print (module_name, 'finished')
