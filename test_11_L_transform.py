module_name = 'test_11_L_transform.py'
print (module_name, 'starting')

from picamera2 import Picamera2
from libcamera import Transform, ColorSpace
from PIL import Image
import time
picam0 = Picamera2(0)
config = picam0.create_video_configuration(
    main={"size": (640, 480), "format": "BGR888"},
    transform=Transform(vflip=True),
    colour_space=ColorSpace(ColorSpace.Sycc()),
    buffer_count=6)
picam0.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})
picam0.configure(config)
picam0.start()
time.sleep(1)

img = picam0.capture_image()
fname = module_name + '.A.jpg'
img.save(fname)

array = picam0.capture_array()
print (array.shape)
img2 = Image.fromarray(array)
fname = module_name + '.B.jpg'
img2.save(fname)

picam0.close()
print (module_name, 'finished')
