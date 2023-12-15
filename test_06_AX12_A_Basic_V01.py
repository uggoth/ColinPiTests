module_name = 'test_06_AX12_A_Basic_V01.py'
print (module_name, 'starting')

from pyax12.connection import Connection

#  To obtain the port name use:    ls /dev/serial/by-path
port_name = 'platform-3f980000.usb-usb-0:1.1.3:1.0-port0'
ax12_connection = Connection(
    port='/dev/serial/by-path/' + port_name,
    baudrate=1000000)

dynamixel_id = 16

ids_available = ax12_connection.scan()

for id in ids_available:
    result = ax12_connection.ping(id)
    if result:
        print (id, 'Available')
    else:
        print (id, '*** NO RESPONSE ***')

ax12_connection.close()

print (module_name, 'finished')
