#!/bin/sh
rm /home/pi/aaa.log
#
sleep 2   #  Must allow time for mysql, pigpiod, etc. etc. to get going
echo starting >> /home/pi/aaa.log
sleep 1
# parameters are:  rpm,  wait time,   stir time   
nohup python3 /home/pi/STIRRER_v02.py 99 999 350 &
sleep 1
echo finished >> /home/pi/aaa.log
