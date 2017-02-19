# Class for calculating and sending signals to thrusters
import helper
import communication

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
        self.force[0] = helper.map(rsy_val, -100, 100, 1140, 1850)
        self.force[1] = helper.map(lsx_val, -100, 100, 1140, 1850)

    def send(self, port):
        """ Convert thruster force values from percent to PWM values and send them.
        """
        communication.send(port, 'T', bytes(force[0] // 100), bytes(force[0] % 100), bytes(force[1] // 100), bytes(force[1] % 100))

    def sendNull(self, port):
        """ Stops all thrusters
        """
        communication.send(port, 'T', bytes(14), bytes(97), bytes(14), bytes(97))
