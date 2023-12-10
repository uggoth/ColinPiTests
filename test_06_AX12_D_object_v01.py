module_name = 'test_06_AX12_D_object_v01.py'

print (module_name, 'starting')

import AX12_Servo_V01 as AX12_Servo
Connection = AX12_Servo.Connection

ax12_connection = Connection(port='/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', baudrate=1000000)

wrist_servo = AX12_Servo.AX12_Servo('Wrist Servo', ax12_connection, 16)

wrist_servo.move_to_and_wait(-100)
wrist_servo.move_to_and_wait(33, 100)
wrist_servo.move_to_and_wait(53, 10)
wrist_servo.move_to_and_wait(100)
wrist_servo.move_to_and_wait(-100, 90)

wrist_servo.close()
ax12_connection.close()
