module_name = 'test_15_E_ESP32_command_stream_v04.py'
print (module_name,'starting')
print ('expects a command processor to be running on the ESP32')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' +
                          ThisPiVersion + '.py').load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' +
                                 data_values['CommandStream'] + '.py').load_module()
import time
import pigpio

gpio = pigpio.pi()
handshake = CommandStream.Handshake('esph', 18, gpio)
esp32_id = 'ZOMBI'
my_esp32 = CommandStream.Pico(esp32_id, gpio, handshake)
if my_esp32.valid:
    commands = ['GETW','WAIT2000','GETW','WHOU']
    i = 0
    for command in commands:
        i += 1
        serial_no_sent = '{:04}'.format(i)
        print ('Sending ' + serial_no_sent + command)
        serial_no_received, feedback, data = my_esp32.send_command(serial_no_sent,command)
        print (serial_no_received, feedback, data)
        time.sleep(1)
else:
    print ('****', esp32_id, 'not found ****')
my_esp32.close()
print (module_name, 'finished')
