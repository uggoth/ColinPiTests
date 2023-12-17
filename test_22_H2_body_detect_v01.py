module_name = 'test_22_H2_body_detect_v01.py'
print (module_name, 'starting')

import cv2
import time
from libcamera import Transform
from picamera2 import Picamera2
classifiers = {'UPPER_BODY':'haarcascade_upperbody',
               'FRONTAL_FACE':'haarcascade_frontalface_default',
               'FULL_BODY':'haarcascade_fullbody'}
which_classifier = 'FULL_BODY'
# NOTE: Need to get XMLs with:    git clone https://github.com/opencv/opencv
classifier_location = '/home/pi/opencv/data/haarcascades/'
classifier_fname = classifier_location + classifiers[which_classifier] + ".xml"
print (classifier_fname)
full_body_detector = cv2.CascadeClassifier(classifier_fname)
cv2.startWindowThread()
picam2 = Picamera2()
config = picam2.create_video_configuration(
    transform=Transform(vflip=True, hflip=True),
    main={"format": 'RGB888', "size": (640, 480)})
#    main={"format": 'RGB888', "size": (1024, 768)})
picam2.align_configuration(config)
print (config)
picam2.configure(config)
picam2.start()
finds = 0
nloops = 50
for i in range(nloops):
    time.sleep(0.1)
    im = picam2.capture_array()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    full_bodys = full_body_detector.detectMultiScale(grey, 1.1, 5)
    if len(full_bodys) > 0:
        print ('found on loop',i+1)
        finds += 1
        for (x, y, w, h) in full_bodys:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))
        cv2.imshow("Camera", im)
        time.sleep(3)
    cv2.imshow("Camera", im)
print ('found',finds,'in',nloops,'loops')
picam2.close()
print (module_name, 'finished')
