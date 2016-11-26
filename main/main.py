# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team
import pygame
import serial
from pygame.locals import *

import thrusterControl
import sensors
import helper
import controller

port = ""     # Used in init() don't change
ser = ""      # Will be defined as a serial port
timeout = 10  # Timeout for communication with Master in seconds

controller = controller.controller()
thruster = thrusterControl.thruster()

def init(port_val = "/dev/ttyACM0" # Change to "COM4" if on Windows, Name of port used to communicate with Arduino
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
    print("Press the 'start' button!")

    n = True
    while n:
        for event in pygame.event.get():
            if event.type == JOYBUTTONDOWN:
                if event.button == 7:
                    print("Connection to controller verified")
                    n = False

    # Verifying conection to the Master Arduino
    ser.write(b'A')
    ser.write(b'm')
    ser.write(b'E')
    read = ser.read(1)
    if read == 'm':
        print("Conection to Master verified")
    else:
        print("Failed to verify connection to Master")
        return

    # Verifying connection to Slave Arduino
    ser.Write(b'A')
    ser.Write(b's')
    ser.Write(b'E')
    read = ser.read(1)
    if read == 's':
        print('Connection to Slave verified')
    else:
        print('Failed to verify connection to Master')


# Code that continiously is being looped through
def main():

    # Following for loop is neccessary only if using Linux
    # Comment out if using Windows
    print("Press and release both triggers!")
    controller.ltrig_val = 1
    controller.rtrig_val = 1
    while controller.ltrig_val != 0 or controller.rtrig_val != 0:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                controller.ltrig_val = round((xbox.get_axis(controller.ltrig) + 1) / 0.02, 0)
                controller.rtrig_val = round((xbox.get_axis(controller.rtrig) + 1) / 0.02, 0)

    while True:

        for event in pygame.event.get():
            # Uppon a button press updates values (states) of all buttons
            # Comment out buttons not used
            if event.type == pygame.JOYBUTTONUP:
                controller.a_butVal = xbox.get_button(controller.a_but)
                controller.b_butVal = xbox.get_button(controller.b_but)
                controller.x_butVal = xbox.get_button(controller.x_but)
                controller.y_butVal = xbox.get_button(controller.y_but)
                controller.l_butVal = xbox.get_button(controller.l_but)
                controller.r_butVal = xbox.get_button(controller.r_but)
                controller.back_butVal = xbox.get_button(controller.back_but)
                controller.start_butVal = xbox.get_button(controller.start_but)
                controller.ls_butVal = xbox.get_button(controller.ls_but)
                controller.rs_butVal = xbox.get_button(controller.rs_but)

            # Uppon joystick movement updates values for all joysticks
            if event.type == pygame.JOYAXISMOTION:
                controller.lsx_val = round(xbox.get_axis(lsx)*100, 0)
                controller.lsy_val = -round(xbox.get_axis(lsy)*100, 0)
                # controller.trig_val = round(xbox.get_axis(trig)*100, 0) uncomment if using Windows
                controller.ltrig_val = -round((xbox.get_axis(ltrig) + 1) / 0.02, 0)  # comment out if using Windows
                controller.rtrig_val = round((xbox.get_axis(rtrig) + 1) / 0.02, 0)   # comment out if using Windows
                controller.rsx_val = round(xbox.get_axis(rsx)*100, 0)
                controller.rsy_val = -round(xbox.get_axis(rsy)*100, 0)

        # Detects and stores direction of left joystick
        # Stores force values of each thruster (in percent of their max F)
        ang = helper.angle(controller.lsx_val, controller.lsy_val)
        pDirection = thruster.direction
 
        thruster.updateForce(controller.rsy_val, controller.lsy_val)

        # If horizontal direction has changed
        # sends zeros to all corner thrusters first
        thruster.sendNull(ser)

        # sends force values of each thruster to Master
        thruster.send(ser)

        if controller.a_butVal == 1:
            print("Humidity:", sensors.get_hum(ser))
 
        if controller.b_butVal == 1:
            print("Temperature:", sensors.get_temp(ser))


init()
main()
