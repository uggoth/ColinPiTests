module_name = 'test_06_AX12_D_object_v01.py'

print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
ax12_code = my_data.params['AX12_Servo']
ax12_path = my_data.params['AX12_PATH']
ax12_speed = my_data.params['AX12_SPEED']
AX12_Servo = SourceFileLoader('ax12_code','/home/pi/ColinPiClasses/' + ax12_code + '.py').load_module()

ax12_connection = AX12_Servo.Connection(port=ax12_path, baudrate=ax12_speed)
wrist_servo = AX12_Servo.AX12_Servo('Wrist Servo', ax12_connection, 20)

wrist_servo.move_to_and_wait(-100)
wrist_servo.move_to_and_wait(33, 100)
wrist_servo.move_to_and_wait(53, 10)
wrist_servo.move_to_and_wait(100)
wrist_servo.move_to_and_wait(-100, 90)
wrist_servo.move_to_and_wait(0, 90)

wrist_servo.close()
ax12_connection.close()
