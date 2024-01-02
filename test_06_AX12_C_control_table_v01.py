module_name = 'test_06_AX12_C_control_table_v01.py'

print (module_name, 'starting')

from pyax12.connection import Connection

from importlib.machinery import SourceFileLoader

colin_data = SourceFileLoader('Colin', '/home/pi/ColinData.py').load_module()
my_data = colin_data.ColinData()
ax12_path = my_data.params['AX12_PATH']
ax12_speed = my_data.params['AX12_SPEED']
ax12_connection = Connection(port=ax12_path, baudrate=ax12_speed)
ax12_list = my_data.params['AX12_LIST']

for dynamixel_id in ax12_list:
    print ('\nDYNAMIXEL ID:',dynamixel_id)
    ax12_connection.pretty_print_control_table(dynamixel_id)

ax12_connection.close()
