module_name = 'test_15_B_USB_reader_v01.py'
print (module_name, 'starting')

import time
import serial
import select

test_port = serial.Serial('/dev/ttyACM0')
for i in range(9):
    inputs, outputs, errors = select.select([test_port],[],[],1)
    if len(inputs) > 0:
        read_text = test_port.readline()
        decoded_text = read_text.decode('utf-8')[:-2]
        print (decoded_text)
    else:
        print ('*** Nothing to read ***')
