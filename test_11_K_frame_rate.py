module_name = 'test_11_K_frame_rate.py'
print (module_name, 'starting')

from picamera2 import Picamera2
import numpy as np
import time

picam0 = Picamera2(0)
config = picam0.create_video_configuration(main={"size": (640, 480)})
picam0.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam0.configure(config)
picam0.start()

picam1 = Picamera2(1)
config = picam1.create_video_configuration(main={"size": (640, 480)})
picam1.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam1.configure(config)
picam1.start()

loops = 30
start = time.time()
for i in range(loops):
  print ('loop',i+1)
  array0 = picam0.capture_array()
  array1 = picam1.capture_array()
duration = time.time() - start
fps = int((loops / duration) + 0.5)
print (loops,'loops   ',fps,'FPS')
picam0.close()

print (module_name, 'finished')
