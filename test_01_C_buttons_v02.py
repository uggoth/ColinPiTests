module_name = 'test_pi_01_C_buttons_v02.py'

import ThisComputer_Georgia_V01 as ThisComputer
time = ThisComputer.time

print (module_name, 'starting')

these_buttons = ThisComputer.TheseButtons()

out_string = "List of buttons in :\n"
for button in these_buttons.button_list:
    button.previous = 'UNKNOWN'
    out_string += '   ' + button.name + "\n"
print (out_string)

for i in range(100):
    time.sleep(0.1)
    for button in these_buttons.button_list:
        current = button.get()
        if current != button.previous:
            print (button.name, current)
            button.previous = current

print (module_name, 'finished')
