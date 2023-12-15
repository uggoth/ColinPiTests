# ColinPiTests

test suite for raspberry pi in Python

Naming Convention:
'test' + no from list + sequence letter + description + version

e.g. test_06_B_arm_servos_v01.py

Note: if multiple (e.g. using radio remote control to control brushed motors)
      use highest number (e.g. 18 not 08)

Note: generally test in sort order, e.g. test_01_A, test_01_B, test_02_A etc.

00 - bsc - basic function tests (no peripherals)
01 - dig - digital inputs
02 - ana - analogue inputs
03 - led - LEDs
04 - snd - sound
05 - stp - stepper motors (also posing)
06 - srv - servo motors (also posing)
07 - mot - brushed motors
08 - blm - brushless motors
09 - flg - flags
10 - imu - IMU
11 - cam - camera
12 - rly - relays (also posing)
13 - myq - MySQL
14 - sys - system and built-in functions
15 - com - command streams
16 - thr - multi-threading
17 - smc - state machines
18 - rrc - radio remote control
19 - obj - object hierarchy
20 - web - webservers
21 - vdu - display
22 - cv2 - OpenCV
23 - bth - BlueTooth
24 - tfl - Tensor Flow Lite
