module_name = 'test_11_C_config.py'
print (module_name, 'starting')
from picamera2 import Picamera2
import time
picam0 = Picamera2(0)
config = picam0.create_video_configuration(main={"size": (640, 480)})
picam0.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam0.configure(config)
picam0.start()
time.sleep(0.1)
array = picam0.capture_array()
print (array.shape)
picam0.close()
print (module_name, 'finished')
