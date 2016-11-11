# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import pygame
import serial
from pygame.locals import *
from time import sleep

from control import *
from helper import *
import sensors

port = ""     # Used in init() don't change
ser = ""      # Will be defined as a serial port
timeout = 10  # Timeout for communication with Master in seconds

control = control()

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
ls_but = 9   # comment out if on Windows
rs_but = 10  # comment out if on Windows

# Xbox controller axis IDs
lsx = 0
lsy = 1
# trig = 2 uncomment if on Windows
ltrig = 2  # comment out if on Windows
rtrig = 5  # comment out if on Windows
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
ltrig_val = 50  # comment out if on Windows
rtrig_val = 50  # comment out if on Windows
rsx_val = 0
rsy_val = 0


def init(port_val = "/dev/ttyACM0",  # Change to "COM4" if on Windows, Name of port used to communicate with Arduino
         ):
    global port
    port = port_val
    global ser
    ser = serial.Serial(port, timeout=timeout)
    pygame.joystick.init()
    global xbox
    xbox = pygame.joystick.Joystick(0)
    xbox.init()
    screen = pygame.display.set_mode((320, 160))
    pygame.display.set_caption("Thruster")
    while not ser.isOpen():  # Waits until port opens
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

    # Verifying conection to the Master Arduino
    ser.write(b'A')
    ser.write(b'A')
    ser.write(b'm')
    ser.write(b'm')
    ser.write(b'E')
    read = ser.read(2)
    if read == 'mm':
        print("Conection to Master verified")
    else:
        print("Failed to verify connection to Master")
        return

    # Verifying connection to Slave Arduino
    ser.Write(b'A')
    ser.Write(b'A')
    ser.Write(b's')
    ser.Write(b's')
    ser.Write(b'E')
    read = ser.read(2)
    if read == 'ss':
        print('Connection to Slave verified')
    else:
        print('Failed to verify connection to Master')


# Code that continiously is being looped through
def main():

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
                ltrig_val = -round((xbox.get_axis(ltrig) + 1) / 0.02, 0)  # comment out if using Windows
                rtrig_val = round((xbox.get_axis(rtrig) + 1) / 0.02, 0)   # comment out if using Windows
                rsx_val = round(xbox.get_axis(rsx)*100, 0)
                rsy_val = -round(xbox.get_axis(rsy)*100, 0)

        # Detects and stores direction of left joystick
        # Stores force values of each thruster (in percent of their max F)
        ang = angle(lsx_val, lsy_val)
        pDirection = control.direction

        control.updateForce(ang, rsy_val, ltrig_val, rtrig_val)

        # If horizontal direction has changed
        # sends zeros to all corner thrusters first
        control.sendNull(ser)

        # sends force values of each thruster to Master
        control.send(ser)

        if a_butVal == 1:
            print("Humidity:", sensors.get_hum(ser))
 
        if b_butVal == 1:
            print("Temperature:", sensors.get_temp(ser))



init()
main()
