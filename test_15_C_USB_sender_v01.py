module_name = 'test_15_C_USB_sender_v01.py'
print (module_name, 'starting')

import time
import serial
import select

test_port = serial.Serial('/dev/ttyACM0')
for i in range(9):
    time.sleep(1)
    in_text = 'loop ' + str(i) + '\n'
    out_text = in_text.encode('utf-8')
    try:
        test_port.write(out_text)
    except:
        print ('write failed')

print (module_name, 'finished')
