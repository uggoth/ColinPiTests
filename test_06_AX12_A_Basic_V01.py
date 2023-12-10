module_name = 'test_06_AX12_A_Basic_V01.py'

print (module_name, 'starting')

from pyax12.connection import Connection

ax12_connection = Connection(port='/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', baudrate=1000000)

dynamixel_id = 16

is_available = ax12_connection.ping(dynamixel_id)

print (is_available)

ax12_connection.close()
