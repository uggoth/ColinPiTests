module_prefix = 'test_05_D_stepping'
module_version = '01'
module_name = module_prefix + '_v' + module_version + '.py'
print (module_name, 'starting')

import tkinter as tk
import pigpio
import time

class ServoPin:
    def __init__(self, name, master, x, y):
        self.master = master
        self.name = name
        self.my_var = tk.StringVar()
        x_now = x
        y_now = y
        x_interval = 50
        y_interval = 50
        self.gpio_list = tk.Spinbox(master, textvariable=self.my_var, width=5, 
                                    values=allowed_gpios)
        self.gpio_list.place(x=x_now, y=y_now)
        self.state = 'OFF'

        y_now += y_interval
        self.on_button = tk.Button(master, text='On', command=self.on)
        self.on_button.place(x=x_now, y=y_now)

        y_now += y_interval
        self.off_button = tk.Button(master, text='Off', command=self.off)
        self.off_button.place(x=x_now, y=y_now)

    def on(self):
        self.state = 'ON'
        gpio.write(int(self.my_var.get()), 1)
        print (str(self.my_var.get()) + ' ' + self.state)
        
    def off(self):
        self.state = 'OFF'
        gpio.write(int(self.my_var.get()), 0)
        print (str(self.my_var.get()) + ' ' + self.state)
        
class Main:
    def __init__(self, name, master, width, height):
        self.master = master
        self.name = name
        self.frame_width = width
        self.frame_height = height
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.owning_object = self
        self.frame.pack()
        x_left = 10
        y_top = 10
        x_interval = 150
        y_interval = 170
        x_now = x_left
        y_now = y_top
        self.pin_1 = ServoPin('Pin 1', self.frame, x_now, y_now)
        x_now += x_interval
        self.pin_2 = ServoPin('Pin 2', self.frame, x_now, y_now)
        x_now += x_interval
        self.pin_3 = ServoPin('Pin 3', self.frame, x_now, y_now)
        x_now += x_interval
        self.pin_4 = ServoPin('Pin 4', self.frame, x_now, y_now)
        x_now = x_left
        y_now += y_interval
        self.setup_button = tk.Button(master, text='Set Up Stepping', command=self.setup)
        self.setup_button.place(x=x_now, y=y_now)
        y_now += y_interval
        self.step_button = tk.Button(master, text='Do one Step', command=self.do_step)
        self.step_button.place(x=x_now, y=y_now)
    def setup(self):
        print ('setting up steps')
        self.pins = [self.pin_1.my_var.get(),self.pin_2.my_var.get(),self.pin_3.my_var.get(),self.pin_4.my_var.get()]
        self.steps = [[1,0,0,0],
                      [1,0,1,0],
                      [0,0,1,0],
                      [0,1,1,0],
                      [0,1,0,0],
                      [0,1,0,1],
                      [0,0,0,1],
                      [1,0,0,1]]
        self.step_index = 0
    def do_step(self):
        step = self.steps[self.step_index]
        print ('Step', self.step_index)
        for i in range(4):
            pin_no = self.pins[i]
            new_state = step[i]
            gpio.write(int(pin_no), new_state)
        self.step_index += 1
        if self.step_index >= len(self.steps):
            self.step_index = 0
                   

gpio = pigpio.pi()
allowed_gpios = (4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27)
for pin_no in allowed_gpios:
    gpio.set_mode(pin_no, pigpio.OUTPUT)
    gpio.write(pin_no, 0)
root = tk.Tk()
root.title('GPIO Testing')
my_main_window = Main('Main Window', root, 750, 590)
root.mainloop()
