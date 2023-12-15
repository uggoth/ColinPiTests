from picamera2 import Picamera2
import time
picam2 = Picamera2()
config = picam2.create_still_configuration({"size": (640, 480)})
picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.configure(config)
picam2.start()
loops = 30
start = time.time()
for i in range(loops):
  metadata = picam2.capture_metadata()
duration = time.time() - start
fps = int((loops / duration) + 0.5)
print (loops,'loops   ',fps,'FPS')
