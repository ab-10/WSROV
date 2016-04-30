# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import serial
import pygame
from pygame.locals import *
import time

# Xbox controller buttons
a_but = 0
b_but = 1
x_but = 2
y_but = 3
l_but = 4
r_but = 5
back_but = 6
start_but = 7
ls_but = 8
rs_but = 9

# Xbox controller axes
lsx = 0
lsy = 1
trig = 2
rsx = 3
rsy = 4

port = ""
ser = ""
timeout = 10

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
        print("Failed to verify connection to master)
        return
            
        
        
# Code that continiously is being looped through
# def main():
    

class CThruster:
    def __init__(self,
                 num,# ID of a thruster
                 lb, # Lower bound of PWM that will be sent to a thruster
                 ub): # Upper bound of PWM that will be sent to a thruster
        self.num = num
        self.lb = lb
        self.ub = ub

    def write(self, signal):
        ser.write(self.num)
        ser.write(self.num)
        ser.write(signal)
        ser.write(signal)
