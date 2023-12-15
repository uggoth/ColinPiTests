module_name = 'test_pi_01_D_wait_for_v01.py'

import ThisComputer_Georgia_V01 as ThisComputer
time = ThisComputer.time

print (module_name, 'starting')

these_buttons = ThisComputer.TheseButtons()
red_button = these_buttons.red_button

if red_button.wait_for(10):
    print ('pressed')
else:
    print ('timed_out')

print (module_name, 'finished')
