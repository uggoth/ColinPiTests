module_name = 'test_22_hsv_calibrate_A_v02.py'
print (module_name,'starting')

import tkinter as tk
import colorsys

def hsv_to_hex(hsv_in): #  hsv_in is an array [h,s,v]
                        #  result is a string of form: '#rrggbb'
        stage_2 = [0] * 3
        for i in range(3):
            stage_2[i] = hsv_in[i] / 255.0
        stage_3 = colorsys.hsv_to_rgb(stage_2[0], stage_2[1], stage_2[2])
        stage_4 = [0] * 3
        for i in range(3):
            stage_4[i] = abs(int(stage_3[i] * 255))
        stage_5 = '#{:02x}{:02x}{:02x}'.format(stage_4[0], stage_4[1], stage_4[2])
        return stage_5
        
class Slider(tk.Scale):
    def callback(self, position):
        # print (self.name, position)
        self.frame.display_swatches()
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
    def __init__(self, master):
        self.master = master
        self.frame_width = 700
        self.frame_height = 700
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.pack()

        x_left = 20
        x_now = x_left
        x_interval = 100
        y_now = 20
        y_interval = 80

        self.hue_low = Slider(master, self, 'Hue Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.hue_high = Slider(master, self, 'Hue High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.saturation_low = Slider(master, self, 'Saturation Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.saturation_high = Slider(master, self, 'Saturation High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.value_low = Slider(master, self, 'Value Low', 0, 255, x_now, y_now, 0)

        y_now += y_interval
        self.value_high = Slider(master, self, 'Value High', 0, 255, x_now, y_now, 255)

        y_now += y_interval
        self.canvas = tk.Canvas(master, height=100, width=400)
        self.low_swatch = self.canvas.create_rectangle(10,10,90,60)
        self.high_swatch = self.canvas.create_rectangle(200,10,290,60)
        self.canvas.place(x=200, y=y_now)
        self.canvas.itemconfig(self.low_swatch, fill='black')
        self.canvas.itemconfig(self.high_swatch, fill='white')
    def display_swatches(self):
        lows_hsv = [self.hue_low.get(), self.saturation_low.get(), self.value_low.get()]
        lows_rgb_hex = hsv_to_hex(lows_hsv)
        self.canvas.itemconfig(self.low_swatch, fill=lows_rgb_hex)
        highs_hsv = [self.hue_high.get(), self.saturation_high.get(), self.value_high.get()]
        highs_rgb_hex = hsv_to_hex(highs_hsv)
        self.canvas.itemconfig(self.high_swatch, fill=highs_rgb_hex)
        

root = tk.Tk()
root.title('Calibrate CSV')
my_calibrator = Calibrator(root)
root.mainloop()
