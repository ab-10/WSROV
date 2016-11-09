# Class for calculating and sending signals to thrusters

class control:
    """ Stores thruster force values and handles sending them.
    """

    force = [none] * 7
    direction = 'none'

    def updateForce(joystickAngle, rsy_val, ltrig_val, rtrig_val):
        """ Updates locally stored thruster force values and direction.

        Arguments:
        joystickAngle -- angle that the coordinate of steering joystick make with the x-axis
        rsy_val -- y value of right joystick
        ltrig_val -- value of left trigger (must be modified for Windows, because on win both triggers are read as single variable)
        rtrig_val -- value of right trigger (also must be modified for Windows)
        """
        if ang >= 45 and ang < 135:
            direction = 'F'
            force[1] = rsy_val
            force[2] = rsy_val
            force[3] = 0
            force[4] = 0
        elif ang >= 135 and ang < 225:
            direction = 'L'
            force[1] = rsy_val
            force[2] = 0
            force[3] = 0
            force[4] = rsy_val
        elif ang >= 225 and ang < 315:
            direction = 'B'
            force[1] = 0
            force[2] = 0
            force[3] = rsy_val
            force[4] = rsy_val
        elif ang >= 315 or ang < 45:
            direction = 'R'
            force[1] = 0
            force[2] = rsy_val
            force[3] = rsy_val
            force[4] = 0
        if ltrig_val != 0:
            force[5] = -ltrig_val
            force[6] = -ltrig_val
        elif rtrig_val != 0:
            force[5] = rtrig_val
            force[6] = rtrig_val

    def send(self, ser):
        """ Convert thruster force values from percent to PWM values and send them.
        """
        for i in range(1, 7):
            force = map(force[i], -100, 100, 1140, 1855)
            force = str(force)
            ser.write(force)
        ser.write('E')

    def sendNull(self, ser):
        """ Stops all thrusters
        """
        ser.write('T')
        ser.write('T')
        for i in range(1, 7):
            force = map(0, -100, 100, 1140, 1855)
            force = str(force)
            ser.write(force)
        ser.write('E')

