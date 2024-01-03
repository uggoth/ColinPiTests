module_name = 'test_06_AX12_B_Scan_V01.py'

print (module_name, 'starting')

from pyax12.connection import Connection

from importlib.machinery import SourceFileLoader

colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
ax12_path = my_data.params['AX12_PATH']
ax12_speed = my_data.params['AX12_SPEED']
ax12_connection = Connection(port=ax12_path, baudrate=ax12_speed)

ids_available = ax12_connection.scan()

for dynamixel_id in ids_available:
    print (dynamixel_id)

ax12_connection.close()
