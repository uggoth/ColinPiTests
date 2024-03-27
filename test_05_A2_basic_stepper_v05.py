module_name = 'test_05_A2_basic_stepper_v05.py'
module_create_date = '202403271013'

print (module_name, 'starting')

from importlib.machinery import SourceFileLoader
colin_data = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
my_data = colin_data.ColinData()
GPIO_version = my_data.params['GPIO']
GPIO = SourceFileLoader('GPIO', '/home/pi/ColinPiClasses/' +
                          GPIO_version + '.py').load_module()
ColObjects_version = my_data.params['ColObjects']
ColObjects = SourceFileLoader('GPIO', '/home/pi/ColinPiClasses/' +
                          ColObjects_version + '.py').load_module()
import pigpio
gpio = pigpio.pi()

test_stepper = GPIO.L298NStepperShort('Test Stepper', gpio, 19, 8, 7, 12)
test_stepper.float()

step_ons = 25   #  50 step_ons = 360 degree rotation
pause_microseconds = 5000

for i in range(step_ons):
#    test_stepper.step_on('CLK', pause_microseconds)
    test_stepper.step_on('ANTI', pause_microseconds)
test_stepper.float()
test_stepper.close()

print (module_name, 'finished')
