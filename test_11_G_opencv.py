module_name = 'test_11_G_opencv.py'
print (module_name, 'starting')

import cv2
print (cv2.__version__)
import time
cam = cv2.VideoCapture(0)
for i in range(5):
        print ('loop',i+1)
        time.sleep(1)
        result, image = cam.read()
        if result:
                break
if result:
        print ('image OK')
        cv2.imshow('testing', image)
        cv2.imwrite('testing.png', image)
else:
        print ('NO image')

cam.close()
print (module_name, 'finished')
