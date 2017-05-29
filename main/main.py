# Thruster - Library for controlling thrusters of WSROV's ROV
# Created by WSROV team

import pygame
import serial
from pygame.locals import *

import thrusterControl
import sensors
import helper
import communication
import controller

port = ""     # port object used in init()

controller = controller.controller()
thruster = thrusterControl.thruster()

def init(port_val = "/dev/ttyACM1",
        timeout=1
         ):
    global port
    port = serial.Serial(port_val, timeout=timeout)
    pygame.joystick.init()
    global xbox
    xbox = pygame.joystick.Joystick(0)
    xbox.init()
    screen = pygame.display.set_mode((320, 160))
    pygame.display.set_caption("WSROV")
    while not port.isOpen():  # Waits until port opens
        pass


def test():
    """ Tests communication with Xbox controller and both Arduinos
    Return: true or false, based on whether the test was successful
    """

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
    print("Verifying connection to Master")
    communication.send(port, 'A', 'm')
    read = communication.read(port)
    print(read)
    if read == b'm':
        print("Conection to Master verified")
    else:
        print("Failed to verify connection to Master")
        return False

    # Verifying connection to Slave Arduino
    communication.send(port, 'A', 's')
    read = communication.read(port)
    print(read)
    if read == b's':
        print('Connection to Slave verified')
    else:
        print('Failed to verify connection to Slave')
        return False

    return True

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
    print("Trigger press has been recorded.")

    while True:

        for event in pygame.event.get():
            # Uppon a button press updates values (states) of all buttons
            # Comment out buttons not used
            if event.type == pygame.JOYBUTTONUP:
                if event.button == controller.a_but:
                    print("Humidity requested")
                    print("Humidity: ", sensors.get_hum(port))
                elif event.button == controller.b_but:
                    print("Temperature requested")
                    print("Temperature: ", sensors.get_temp(port))

            # Uppon joystick movement updates values for all joysticks
            if event.type == pygame.JOYAXISMOTION:
                controller.lsx_val = round(xbox.get_axis(controller.lsx)*100, 0)
                controller.lsy_val = -round(xbox.get_axis(controller.lsy)*100, 0)
                # controller.trig_val = round(xbox.get_axis(trig)*100, 0) uncomment if using Windows
                controller.ltrig_val = -round((xbox.get_axis(controller.ltrig) + 1) / 0.02, 0)  # comment out if using Windows
                controller.rtrig_val = round((xbox.get_axis(controller.rtrig) + 1) / 0.02, 0)   # comment out if using Windows
                controller.rsx_val = round(xbox.get_axis(controller.rsx)*100, 0)
                controller.rsy_val = -round(xbox.get_axis(controller.rsy)*100, 0)

        # Detects and stores direction of left joystick
        # Stores force values of each thruster (in percent of their max F)
        ang = helper.angle(controller.lsx_val, controller.lsy_val)
        pDirection = thruster.direction

        thruster.updateForce(controller.rsy_val, controller.lsy_val)

        # If horizontal direction has changed
        # sends zeros to all corner thrusters first
        thruster.sendNull(port)

        # sends force values of each thruster to Master
        thruster.send(port)


init()
test()
main()
