module_name = 'test_01_E_DIP_switches_v03.py'
print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
my_computer = SourceFileLoader('Colin', '/home/pi/ColinThisPi/' + my_data.params['ThisPi'] + '.py').load_module()
my_dips = my_computer.DIPS()
import time

out_string = "List of dips in :\n"
for dip in my_dips.DIP_list:
    dip.previous = 'UNKNOWN'
    out_string += '   ' + dip.name + "\n"
print (out_string)

for i in range(100):
    time.sleep(0.1)
    for dip in my_dips.DIP_list:
        current = dip.get()
        if current != dip.previous:
            print (dip.name, dip.description, current)
            dip.previous = current

print (module_name, 'finished')
