# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import serial
import pygame
from pygame.locals import *
from math import atan
from time import sleep

port = ""     # Used in init() don't change
ser = ""      # Will be defined as a serial port
timeout = 10  # Timeout for communication with Master in seconds

# Maps input  to given parameters
# as the map() function in Arduino Programming Language
def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def init(port_val = "COM4", # Change to "/dev/ttyACM0" if on Linux, Name of port used to communicate with Arduino
         ):
    # global port
    # port = port_val
    # global ser
    # ser = serial.Serial(port, timeout = timeout)
    pygame.joystick.init()
    global xbox
    xbox = pygame.joystick.Joystick(0)
    xbox.init()
    screen = pygame.display.set_mode((320, 160))
    pygame.display.set_caption("Thruster")
    # while(not ser.isOpen()): # Waits until port opens
        # pass

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

    # Verifying conection to the Master Arduino
    ser.write(b'A')
    ser.write(b'A')
    ser.write(b'm')
    ser.write(b'm')
    ser.write(b'E')
    read = ser.read(2)
    if(read == 'mm'):
        print("Conection to Master verified")
    else:
        print("Failed to verify connection to Master")
        return

def angle(x, y):
    if x == 0:
        if y < 0:
            return 270
        if y > 0:
            return 90
        else:
            return 0
    tan  = y / x
    arctan = atan(tan) / 3.14 * 180
    if x > 0 and y >= 0:
        return arctan
    elif x > 0 and y < 0:
        return arctan + 360
    elif x < 0 and y <= 0:
        return arctan + 180
    elif x < 0 and y > 0:
        arctan + 180

# Code that continiously is being looped through
def main():

    thrusters = [None]*7
    tForce = [None]*7 # contains the force values for each thruster in percent
                      # can be both positive and negative

    n = 1
    while(n <= 6):
        thrusters[n] = Thruster(n)
        n += 1
    direction = 'none'
    pDirection = 'none'
    # Xbox controller button IDs
    a_but = 0
    b_but = 1
    x_but = 2
    y_but = 3
    l_but = 4
    r_but = 5
    back_but = 6
    start_but = 7
    # ls_but = 8 uncomment if on Windows
    # rs_but = 9 uncomment if on Windows
    ls_but = 9 # comment out if on Windows
    rs_but = 10 # comment out if on Windows

    # Xbox controller axis IDs
    lsx = 0
    lsy = 1
    # trig = 2 uncomment if on Windows
    ltrig = 2 # comment out if on Windows
    rtrig = 5 # comment out if on Windows
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
    lsx_val = 0
    lsy_val = 0
    # trig_val = 0 uncomment if on Windows
    ltrig_val = 50 # comment out if on Windows
    rtrig_val = 50 # comment out if on Windows
    rsx_val = 0
    rsy_val = 0

    # Following for loop is neccessary only if using Linux
    # Comment out if using Windows
    print("Press and release both triggers!")
    while ltrig_val != 0 or rtrig_val != 0:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                ltrig_val = round((xbox.get_axis(ltrig) + 1) / 0.02, 0)
                rtrig_val = round((xbox.get_axis(rtrig) + 1) / 0.02, 0)

    while True:
        for event in pygame.event.get():
            # Uppon a button press updates values (states) of all buttons
            # Comment out buttons not used
            if event.type == pygame.JOYBUTTONUP:
                a_butVal = xbox.get_button(a_but)
                b_butVal = xbox.get_button(b_but)
                x_butVal = xbox.get_button(x_but)
                y_butVal = xbox.get_button(y_but)
                l_butVal = xbox.get_button(l_but)
                r_butVal = xbox.get_button(r_but)
                back_butVal = xbox.get_button(back_but)
                start_butVal = xbox.get_button(start_but)
                ls_butVal = xbox.get_button(ls_but)
                rs_butVal = xbox.get_button(rs_but)
            # Uppon joystick movement updates values for all joysticks
            if event.type == pygame.JOYAXISMOTION:
                lsx_val = round(xbox.get_axis(lsx)*100, 0)
                lsy_val = -round(xbox.get_axis(lsy)*100, 0)
                # trig_val = round(xbox.get_axis(trig)*100, 0) uncomment if using Windows
                ltrig_val = round((xbox.get_axis(ltrig) + 1) / 0.02, 0) # comment out if using Windows
                rtrig_val = round((xbox.get_axis(rtrig) + 1) / 0.02, 0) # comment out if using Windows
                rsx_val = round(xbox.get_axis(rsx)*100, 0)
                rsy_val = -round(xbox.get_axis(rsy)*100, 0)
        # Detects and stores direction of left joystick
        # Stores force values of each thruster (in percent of their max F)
        ang = angle(lsx_val, lsy_val)
        pDirection = direction
        if ang >= 45 and ang < 135:
            direction = 'F'
            tForce[1] = rsy_val
            tForce[2] = rsy_val
            tForce[3] = 0
            tForce[4] = 0
        elif ang >= 135 and ang < 225:
            direction = 'L'
            tForce[1] = rsy_val
            tForce[2] = 0
            tForce[3] = 0
            tForce[4] = rsy_val
        elif ang >= 225 and ang < 315:
            direction = 'B'
            tForce[1] = 0
            tForce[2] = 0
            tForce[3] = rsy_val
            tForce[4] = rsy_val
        elif ang >= 315 or ang < 45:
            direction = 'R'
            tForce[1] = 0
            tForce[2] = rsy_val
            tForce[3] = rsy_val
            tForce[4] = 0
        if ltrig_val != 0:
            tForce[5] = -ltrig_val
            tForce[6] = -ltrig_val
        elif rtrig_val != 0:
            tForce[5] = rtrig_val
            tForce[6] = rtrig_val

        # If horizontal direction has changed
        # sends zeros to all corner thrusters first
        if direction != pDirection:
            n = 1
            while n <= 4:
                thrusters[n].send(0)
                n += 1
        # sends force values of each thruster to Master
        for n, thruster in enumerate(thrusters):
            thruster.send(tForce(n))
		ser.write('E')
		ser.write('E')

# Class that defines properties for each individual thruster
class Thruster:
# Function automatically executed upon creation of a thruster object
    def __init__(self,
                 num,# ID of a thruster
                 lb = 1140, # Lower bound of PWM that will be sent to a thruster
                 ub = 1855): # Upper bound of PWM that will be sent to a thruster
        self.num = num
        self.lb = lb
        self.ub = ub

# Function to send values to an ESC through Arduinos
    def send(self, force):
        signal = arduino_map(force, -100, 100, self.lb, self.ub)
        ser.write(self.num)
        ser.write(self.num)
        ser.write(signal)
        ser.write(signal)

init()
main()
