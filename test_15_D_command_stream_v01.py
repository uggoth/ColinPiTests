module_name = 'test_15_D_command_stream_v01.py'
print (module_name,'starting')
print ('expects test_15_D to be running on the Pico')

import CommandStreamPi_v03 as CommandStream
import time
import pigpio

gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)

time.sleep(1)
my_pico.close()
print (module_name, 'finished')
