module_name = 'test_22_face_detection.py'
print ('\n\n', module_name, 'starting')
import cv2
import time
from picamera2 import Picamera2
classifiers = {'UPPER_BODY':'haarcascade_upperbody',
               'FRONTAL_FACE':'haarcascade_frontalface_default',
               'FULL_BODY':'haarcascade_fullbody'}
which_classifier = 'FULL_BODY'
classifier_location = '/home/pi/opencv/data/haarcascades/'
classifier_fname = classifier_location + classifiers[which_classifier] + ".xml"
print (classifier_fname)
face_detector = cv2.CascadeClassifier(classifier_fname)
cv2.startWindowThread()
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
for i in range(100):
    time.sleep(0.1)
    print ('loop',i+1)
    im = picam2.capture_array()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))
    cv2.imshow("Camera", im)
