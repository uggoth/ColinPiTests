module_name = 'test_11_A_basic_camera.py'
print (module_name, 'starting')
from picamera2 import Picamera2
import time
picam2 = Picamera2()
fname = module_name + '.jpg'
picam2.start_and_capture_file(fname)
picam2.close()
print (module_name, 'finished')
