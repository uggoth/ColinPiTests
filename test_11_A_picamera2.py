module_prefix = 'test_11_A_picamera2'
module_name = module_prefix + '_v02.py'
print (module_name, 'starting')
from picamera2 import Picamera2 #, Preview
import libcamera
import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
                                                  transform=libcamera.Transform(hflip=1, vflip=1),
                                                  lores={"size": (640, 480)},
                                                  display="lores")
picam2.configure(camera_config)
# can't preview in VNC
# picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(1)
fname = module_prefix + '.jpg'
picam2.capture_file(fname)
picam2.close()
print (module_name, 'finished')
