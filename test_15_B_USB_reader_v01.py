module_name = 'test_15_B_USB_reader_v01.py'
print (module_name, 'starting')

import time
import serial
import select

test_port = serial.Serial('/dev/ttyACM1', baudrate=115200,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE)
previous = 999
for i in range(1000000):
    inputs, outputs, errors = select.select([test_port],[],[],1)
    if len(inputs) > 0:
        if i % 20 == 0:
            read_text = test_port.readline()
            decoded_text = read_text.decode('utf-8')[:-2]
            try:
                this = int(int(decoded_text) / 5)
            except:
                continue
            if this != previous:
                print ('Pico Sends:',decoded_text)
                previous = this
    else:
        print ('*** Nothing to read ***')
