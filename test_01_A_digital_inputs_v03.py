import gpiozero
#pin2 = gpiozero.DigitalInputDevice(2, pull_up=True)

import time

module_name = 'test_01_A_digital_inputs_v02.py'

print (module_name, "starting")
print ("")

pin_no_list = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,26,27]

gpios = []
for pin_no in pin_no_list:
    gpios.append(gpiozero.DigitalInputDevice(pin_no, pull_up=True))

output = ''
for i in range(len(pin_no_list)):
    output += "{0:02d} ".format(pin_no_list[i])
print (output)

for i in range(20):
    output = ' '
    for j in range(len(gpios)):
        output += str(gpios[j].value) + "  "
    print (output)
    time.sleep(2)

print ("")
print (module_name, "finished")
