# Class for calculating and sending signals to thrusters
import helper

class thruster:
    """ Stores thruster force values and handles sending them.
    """

    force = [None] * 2
    direction = 'none'

    def updateForce(self, rsy_val, lsx_val):
        """ Updates locally stored thruster force values and direction.

        Arguments:
        joystickAngle -- angle that the coordinate of steering joystick make with the x-axis
        rsy_val -- y value of right joystick
        ltrig_val -- value of left trigger (must be modified for Windows, because on win both triggers are read as single variable)
        rtrig_val -- value of right trigger (also must be modified for Windows)
        """
        self.force[0] = rsy_val
        self.force[1] = lsx_val

    def send(self, ser):
        """ Convert thruster force values from percent to PWM values and send them.
        """
        for i in range(0, 2):
            force = helper.map(self.force[i], -100, 100, 1140, 1855)
            force = str(force)
            ser.write(force)
        ser.write('E')

    def sendNull(self, ser):
        """ Stops all thrusters
        """
        ser.write('T')
        ser.write('T')
        for i in range(0, 2):
            force = helper.map(0, -100, 100, 1140, 1855)
            force = str(force)
            ser.write(force)
        ser.write('E')

