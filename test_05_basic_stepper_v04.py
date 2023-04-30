module_name = 'test_05_basic_stepper_v03.py'
module_create_date = '202304291713'

print (module_name, 'starting')

import ColObjects_v13 as ColObj
import GPIOPi_v44 as GPIO
test_stepper = GPIO.L298NStepperShort('Test Stepper', 6, 13, 19, 26)
test_stepper.float()
million = 1000000.0
seconds_per_minute = 60.0
steps_per_rev = 200.0
steps_per_step_on = 8.0

revs_per_minute = 99.0
print ('\ninput rpm',revs_per_minute)
duration_seconds = 5.0
print ('input duration',duration_seconds)

revs_per_second = revs_per_minute / seconds_per_minute
print ('\nrps',revs_per_second)
total_revs = duration_seconds * revs_per_second
print ('revs', total_revs)

steps_per_second = revs_per_second * steps_per_rev
print ('sps',steps_per_second)
step_ons_per_second = steps_per_second / steps_per_step_on
print ('sops',step_ons_per_second)

pause_microseconds = int(million / steps_per_second)
print ('pause',pause_microseconds)

step_ons = int(duration_seconds * step_ons_per_second)
print ('step_ons',step_ons)

calc_duration = step_ons * (pause_microseconds * steps_per_step_on / million)
print ('calculated duration',calc_duration)

for i in range(step_ons):
    test_stepper.step_on('CLK', pause_microseconds)
test_stepper.close()

print (module_name, 'finished')
