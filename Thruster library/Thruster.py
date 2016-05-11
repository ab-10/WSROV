# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import serial
import pygame
from pygame.locals import *
import time

# Xbox controller button IDs
a_but = 0
b_but = 1
x_but = 2
y_but = 3
l_but = 4
r_but = 5
back_but = 6
start_but = 7
ls_but = 8 # change to 9 if using linux
rs_but = 9 # change to 10 if using linux

# Xbox controller axis IDs
lsx = 0
lsy = 1
trig = 2
rsx = 3
rsy = 4

# Xbox controller button values (states)
a_butVal = 0
b_butVal = 0
x_butVal = 0
y_butVal = 0
l_butVal = 0
r_butVal = 0
back_butVal = 0
start_butVal = 0
ls_butVal = 0
rs_butVal = 0

# Xbox controller axis values
lsxVal = 0
lsyVal = 0
trigVal = 0
rsxVal = 0
rsyVal = 0

port = ""     # Used in init() don't change
ser = ""      # Will be defined as a serial port
timeout = 10  # Timeout for communication with Master in seconds

def init(port_val = "COM4", # Name of port used to communicate with Arduino
         ):
    global port
    port = port_val
    global ser
    ser = serial.Serial(port, timeout = timeout)
    pygame.joystick.init()
    xbox = pygame.joystick.Joystick(0)
    xbox.init()
    screen = pygame.display.set_mode((320, 160))
    pygame.display.set_caption("Thruster")
    while(not ser.isOpen()): # Waits until port opens
        pass

# Tests whether is it able to communicate to Xbox controller and both Arduinos
def test():
    # Testing connection to the controller
    if(pygame.joystick.get_count() == 0):
        print("No controller found")
        return
    n = 1
    print("Press the 'start' button!")
    while n:
        for event in pygame.event.get():
            if event.type == JOYBUTTONDOWN:
                if event.button == 7:
                    print("Connection to controller verified")
                    n -= 1

    # Verifying conection to the master Arduino
    ser.write(b'A')
    ser.write(b'A')
    ser.write(b'm')
    ser.write(b'm')
    ser.write(b'E')
    read = ser.read(2)
    if(read == 'mm'):
        print("Conection to master verified")
    else:
        print("Failed to verify connection to master")
        return



# Code that continiously is being looped through
def main():
    for event in pygame.event.get():
        # Uppon a button press updates values (states) of all buttons
        # Comment out buttons not used
        if event.type == JOYBUTTONUP:
            a_butVal = get_button(a_but)
            b_butVal = get_button(b_but)
            x_butVal = get_button(x_but)
            y_butVal = get_button(y_but)
            l_butVal = get_button(l_but)
            r_butVal = get_button(r_but)
            back_butVal = get_button(back_but)
            start_butVal = get_button(start_but)
            ls_butVal = get_button(ls_but)
            rs_butVal = get_button(rs_but)
        # Uppon joystick movement updates values for all joysticks
        if event.type == JOYAXISMOTION:
            lsxVal = get_axis(lsx)
            lsyVal = get_axis(lsy)
            trigVal = get_axis(trig)
            rsxVal = get_axis(rsx)
            rsyVal = get_axis(rsy)
    print(lsxVal, " ", lsyVal)

# Class that defines properties for each individual thruster
class Thruster:
# Function automatically executed upon creation of a thruster object
    def __init__(self,
                 num,# ID of a thruster
                 lb, # Lower bound of PWM that will be sent to a thruster
                 ub): # Upper bound of PWM that will be sent to a thruster
        self.num = num
        self.lb = lb
        self.ub = ub

# Function to write values to an ESC through Arduinos
    def write(self, signal):
        ser.write(self.num)
        ser.write(self.num)
        ser.write(signal)
        ser.write(signal)
