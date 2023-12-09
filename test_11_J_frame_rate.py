module_name = 'test_11_J_frame_rate.py'
print (module_name, 'starting')

from picamera2 import Picamera2
import time
picam0 = Picamera2(0)
config = picam0.create_video_configuration(main={"size": (640, 480)})
picam0.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam0.configure(config)
picam0.start()
loops = 30
start = time.time()
for i in range(loops):
  array = picam0.capture_array()
  #print (array.shape)
duration = time.time() - start
fps = int((loops / duration) + 0.5)
print (loops,'loops   ',fps,'FPS')
picam0.close()

print (module_name, 'finished')
