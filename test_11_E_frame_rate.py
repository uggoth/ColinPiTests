from picamera2 import Picamera2
import time
def pprint(modes):
  for mode in modes:
    print (' ')
    for key in mode:
      print (key,':',mode[key])
picam2 = Picamera2()
pprint (picam2.sensor_modes)
width = 640
height = 480
config = picam2.create_still_configuration({'size':(width,height), 'format':'YUV420'}, buffer_count=2)
picam2.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam2.align_configuration(config)
picam2.configure(config)
picam2.start()
loops = 30
start = time.time()
for i in range(loops):
  array = picam2.capture_array()
duration = time.time() - start
fps = int((loops / duration) + 0.5)
print (loops,'loops   ',fps,'FPS')
picam2.close()
