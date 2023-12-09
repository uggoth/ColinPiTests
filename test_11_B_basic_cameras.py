module_name = 'test_11_B_basic_cameras.py'
print (module_name, 'starting')
from picamera2 import Picamera2
import pprint

global_camera_info = Picamera2.global_camera_info()
for camera in global_camera_info:
    pprint.pprint(camera)
    cnum = camera['Num']
    camera['instance'] = Picamera2(cnum)
    fname = module_name + '_' + str(cnum) + '.jpg'
    camera['instance'].start_and_capture_file(fname)
    camera['instance'].close()

print (module_name, 'finished')
