module_name = 'test_22_C_colour_calibrate_v03.py'
print (module_name,'starting')

import tkinter as tk
import cv2
print (cv2.__version__)
import time
from picamera2 import Picamera2
from libcamera import Transform, ColorSpace
from libcamera import controls
from PIL import Image
from PIL import ImageTk
#  may need:    sudo apt install python3-pil.imagetk
import numpy as np

class Slider(tk.Scale):
    def callback(self, position):
        a=1
        # print (self.name, position)
        self.frame.display_result()
    def __init__(self, master, frame, name, low, high, x, y, start):
        self.master = master
        self.frame = frame
        self.name = name
        self.my_var = tk.IntVar()
        super().__init__(master, from_=low, to=high, length=500, sliderlength=20,
                         variable=self.my_var, orient=tk.HORIZONTAL, label=name,
                         command = self.callback)
        self.set(start)
        self.place(x=x, y=y)

class Calibrator:
    def __init__(self, master, mode):
        self.master = master
        self.mode = mode  #  mode is 0 for BGR or 1 for YUV
        self.frame_width = 700
        self.frame_height = 920
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.pack()

        self.labels = []
        m0 = ['B (Blue)','G (Green)','R (Red)']
        self.labels.append(m0)
        m1 = ['Y (Luma)','U (Chroma Blue)','V (Chroma Red)']
        self.labels.append(m1)
        m2 = ['H (Hue)','S (Saturation)','V (Value)']
        self.labels.append(m2)

        x_left = 20
        x_now = x_left
        x_interval = 100
        y_now = 20
        y_interval = 60

        self.factor_1_low = Slider(master, self, self.labels[mode][0] + ' Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.factor_2_low = Slider(master, self, self.labels[mode][1] + ' Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.factor_3_low = Slider(master, self, self.labels[mode][2] + ' Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval * 1.3
        self.factor_1_high = Slider(master, self, self.labels[mode][0] + ' High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.factor_2_high = Slider(master, self, self.labels[mode][1] + ' High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.factor_3_high = Slider(master, self, self.labels[mode][2] + ' High', 0, 255, x_now, y_now, 255)

        y_now += y_interval * 1.3
        self.canvas = tk.Canvas(master, height=480, width=640)
        self.canvas.place(x=x_left, y=y_now)
        img_10 = picam0.capture_array()
        img_20 = Image.fromarray(img_10)
        img_30 = ImageTk.PhotoImage(img_20)
        self.image_container = self.canvas.create_image(0,0,anchor="nw",image=img_30)
        self.canvas.itemconfig(self.image_container, image=img_30)

    def display_result(self):
        global timer_previous, loop_counter, picam0
        timer_now = time.time()
        if (timer_now - timer_previous) > timer_interval:
            img_00 = picam0.capture_array()
            if self.mode == 0:
                img_05 = img_00
            elif self.mode == 1:
                img_05 = cv2.cvtColor(img_00, cv2.COLOR_BGR2YUV)
            elif self.mode == 2:
                img_05 = cv2.cvtColor(img_00, cv2.COLOR_BGR2HSV)
            lows_rgb = np.array([self.factor_1_low.get(), self.factor_2_low.get(), self.factor_3_low.get()], dtype="uint8")
            highs_rgb = np.array([self.factor_1_high.get(), self.factor_2_high.get(), self.factor_3_high.get()], dtype="uint8")
            mask = cv2.inRange(img_05,lows_rgb, highs_rgb)
            #img_10 = cv2.bitwise_and(img_05, img_05, mask=mask)
            img_10 = img_05
            timer_previous = timer_now

            loop_counter += 1
            cv2.putText(img_10,str(loop_counter),
                        (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255,255,0),
                        2,cv2.LINE_AA)
            if self.mode == 0:
                img_15 = img_10
            elif self.mode == 1:
                img_15 = cv2.cvtColor(img_10, cv2.COLOR_YUV2BGR)
            elif self.mode == 2:
                img_15 = cv2.cvtColor(img_10, cv2.COLOR_HSV2BGR)
            img_17 = cv2.bitwise_and(img_15, img_15, mask=mask)
            img_20 = Image.fromarray(img_17)
            img_30 = ImageTk.PhotoImage(img_20)
            self.canvas.itemconfig(self.image_container, image=img_30)
            #self.image_container.refresh()
            #self.image_container.update()
            #self.canvas.refresh()
            #self.canvas.update()
            self.refresh()
            #self.update()
            #self.master.refresh()
            #self.master.update()

picam0 = Picamera2(0)  #  Left camera
config = picam0.create_video_configuration(
    main={"size": (640, 480), "format": "BGR888"},
    transform=Transform(vflip=True),
    colour_space=ColorSpace(ColorSpace.Sycc()),
    buffer_count=6)
#config = picam0.create_video_configuration(
#    main={"size": (640, 480), "format": "YUV420"},
#    transform=Transform(vflip=True),
#    colour_space=ColorSpace(ColorSpace.Sycc()),
#    buffer_count=6)
picam0.set_controls({"ExposureTime": 1000})
picam0.set_controls({"AnalogueGain": 1.0})
#picam0.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam0.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 1.0})
picam0.configure(config)
picam0.start()
time.sleep(1)

root = tk.Tk()
root.title(module_name)
modes = {'BGR':0, 'YUV':1, 'HSV':2}

###################### parameter #################
which_mode = 'HSV'

my_calibrator = Calibrator(root, modes[which_mode])
cv2.startWindowThread()
timer_previous = time.time()
timer_interval = 2.0
loop_counter = 0

root.mainloop()

picam0.close()
print (module_name, 'finished')
